import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import os
import logging
from datetime import datetime
from time import perf_counter

from openai import OpenAI
from dotenv import load_dotenv

from tenacity import (
    retry,
    retry_if_exception_type,
    wait_exponential,
    stop_after_attempt,
    before_sleep_log
)

from config.config import AgentConfig
from config.logger import generate_run_id
from utils.tools import tool_map, tools
from utils.metrics import AgentMetrics
from utils.ctx_manager import ContextWindowManager, ConversationManager

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL"),
)

# ---------------------------------------------------------------------
# Custom Error Types (VERY IMPORTANT)
# ---------------------------------------------------------------------

class TransientLLMError(TypeError):
    """Retryable LLM failure (timeouts, 5xx, parsing issues)"""


class FatalLLMError(RuntimeError):
    """Non-retryable LLM failure"""

# AGENT BASE CLASS
class Agent:
    def __init__(self, config: AgentConfig, logger):
        self.logger = logger
        self.model = config.model
        self.max_iterations = config.max_iterations
        self.max_tokens = config.max_tokens_per_call
        self.temperature = config.temperature
        self.max_context_tokens = config.max_context_tokens
        self.require_approval = config.require_approval

        self.allowed_tools = [
            tool for tool in tools
            if tool["function"]["name"] in config.allowed_tools
        ]


    @retry(
        retry=retry_if_exception_type(TransientLLMError),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        stop=stop_after_attempt(3),
        reraise=True,
        before_sleep=before_sleep_log(logging.getLogger("agent"), logging.WARNING),
    )
    def _call_llm(self, messages):
        """
        One LLM call.
        Retries ONLY for transient failures.
        """

        try:
            self.logger.info("📡 Calling LLM")
            return client.chat.completions.create(
                model=self.model,
                temperature=self.temperature,
                tools=self.allowed_tools,
                tool_choice="auto",
                messages=messages,
                max_tokens=self.max_tokens,
            )

        except TypeError as e:
            # Retryable
            raise TransientLLMError(str(e))

        except Exception as e:
            # Non-retryable
            raise FatalLLMError(str(e))


    def _execute(self, query: str, conversation_id: str):
        metrics = AgentMetrics()
        metrics.start_time = datetime.now()

        messages = ConversationManager().get_or_create(conversation_id)
        messages.append({"role": "user", "content": query})

        for iteration in range(self.max_iterations):
            metrics.iterations = iteration + 1

            self.logger.info(
                "Iteration start",
                extra={"iteration": iteration + 1}
            )

            # Context management
            messages = ContextWindowManager().truncate_messages(
                messages=messages,
                max_tokens=self.max_context_tokens,
            )

            # print(
            #     f"📝 Context: "
            #     f"{ContextWindowManager().count_tokens(messages)} tokens, "
            #     f"{len(messages)} messages"
            # )

            try:
                response = self._call_llm(messages)
            
            # v1
            # except FatalLLMError as e:
            #     metrics.log_error(f"Fatal LLM error: {e}")    
            #     metrics.end_time = datetime.now()
            #     return {      
            #         "output": None,
            #         "error": "Fatal LLM failure",
            #         "metrics": metrics.get_summary(),
            #     }

            # except Exception as e:
            #     metrics.log_error(f"LLM failed after retries: {e}")
            #     metrics.end_time = datetime.now()
            #     return {
            #         "output": None,
            #         "error": "LLM unavailable after retries",
            #         "metrics": metrics.get_summary(),
            #     }

            # v2
            except FatalLLMError as e:
                self.logger.error("Fatal LLM error", extra={"error": str(e)})
                metrics.log_error(str(e))
                break

            except Exception as e:
                self.logger.error("LLM failed after retries", extra={"error": str(e)})
                metrics.log_error(str(e))
                break

            if getattr(response, "usage", None):
                metrics.tokens_used += response.usage.total_tokens

            message = response.choices[0].message

            # ----------------------------------------------------------
            # NO TOOL CALL → FINAL ANSWER
            # ----------------------------------------------------------

            if not message.tool_calls:
                messages.append(
                    {"role": "assistant", "content": message.content}
                )
                metrics.end_time = datetime.now()
                return {
                    "output": message.content,
                    "metrics": metrics.print_summary(),
                }


            for tool_call in message.tool_calls:
                tool_name = tool_call.function.name

                self.logger.info(
                    "Tool call",
                    extra={
                        "tool": tool_name,
                        "iteration": iteration + 1,
                    },
                )
                
                # if tool_name not in [t["function"]["name"] for t in self.allowed_tools]:
                #     raise RuntimeError(f"Tool not allowed: {tool_name}")

                # print(f"🔧 Calling tool: {tool_name}")

                try:
                    func, input_model = tool_map[tool_name]
                    args = input_model.model_validate_json(
                        tool_call.function.arguments
                    )

                    metrics.log_tool_call(tool_name, args.model_dump())

                    start_time = perf_counter()
                    result = func(**args.model_dump())
                    latency_ms = (perf_counter() - start_time) * 1000
                    metrics.log_tool_latency(tool_name, latency_ms)
                    
                    self.logger.info(
                        "Tool executed",
                        extra={
                            "tool": tool_name,
                            "latency_ms": latency_ms,
                            "iteration": iteration + 1,
                        }
                    )
                    
                    messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": str(result),
                        }
                    )

                    print("   ✓ Tool success")

                except Exception as e:
                    error_msg = f"Tool {tool_name} failed: {e}"
                    self.logger.error(
                        "Tool execution failed",
                        extra={
                            "tool": tool_name,
                            "error": str(e)
                        }
                    )
                    metrics.log_error(error_msg)

                    messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": error_msg,
                        }
                    )

        # -----------------------------------------------------------------
        # MAX ITERATIONS EXCEEDED
        # -----------------------------------------------------------------

        metrics.end_time = datetime.now()
        return {
            "output": None,
            "error": "Max iterations reached",
            "metrics": metrics.get_summary(),
        }

    def run(self, query: str, conversation_id: str):
        run_id = generate_run_id()
        
        self.logger = logging.LoggerAdapter(
            self.logger,
            {"run_id": run_id, "conversation_id": conversation_id}
        )
        
        self.logger.info("Agent run started")
        return self._execute(query, conversation_id)

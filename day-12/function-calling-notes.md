# Function Calling Notes

## Why LLMs Need Tools
An LLM is fundamentally a text predictor — it generates the next likely word based on patterns learned during training. It doesn't have a calculator, doesn't have live internet access, and doesn't have a live connection to any database. So if you ask it "what's 4382 × 9021" or "what's today's stock price," it can only guess based on patterns, not actually compute or fetch the real answer. This is exactly the kind of thing that leads to hallucination — confidently wrong answers on things outside pure language reasoning.

## How a Tool Fixes This
Instead of trying to answer directly, the model can be given a list of "tools" it's allowed to call — real functions with real code behind them (a calculator, a search engine, a database query). When the model recognizes a question needs a tool, instead of guessing an answer, it outputs a structured request (JSON) saying which tool to run and with what input. Your code then actually runs that function, gets a real result, and hands that result back to the model — which then uses the real data to write its final answer. This turns the model from "a guesser" into "a reasoner that knows when to ask for real data."

## JSON Schema Concept
A tool is described to the model using a JSON schema with 3 main parts:
- **name** – what the tool is called (e.g. `get_weather`)
- **description** – what it does, so the model knows when to use it
- **parameters** – what inputs it needs, and their types (e.g. `city: string`)

The model doesn't run the function itself — it just outputs JSON saying "call `get_weather` with `city: Mumbai`," and your code is responsible for actually executing that and returning the result.

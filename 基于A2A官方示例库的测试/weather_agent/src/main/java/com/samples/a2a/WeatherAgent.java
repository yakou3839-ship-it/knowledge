package com.samples.a2a;

import jakarta.enterprise.context.ApplicationScoped;

import dev.langchain4j.service.SystemMessage;
import dev.langchain4j.service.UserMessage;
import io.quarkiverse.langchain4j.RegisterAiService;
import io.quarkiverse.langchain4j.mcp.runtime.McpToolBox;

/**
 * Weather agent interface that provides weather forecast assistance.
 */
@RegisterAiService
@ApplicationScoped
public interface WeatherAgent {

    /**
     * Processes a weather-related question and returns a response.
     *
     * @param question the user's weather question
     * @return the weather information response
     */
    @SystemMessage("""
            You are a specialized China weather forecast assistant for travel planning.
            Use the provided MCP tool to fetch daily forecasts for every date in the
            requested date range. Summarize each day in Chinese with weather,
            high/low temperature, precipitation probability and amount, and wind.
            Recommend the best travel day(s) based on: no precipitation,
            precipitation probability below 50%, and temperatures between 10 and
            30 degrees Celsius. You must rely exclusively on tool output and never
            invent data. If the tool says the requested dates are outside its
            forecast window, directly state the tool-provided current date and
            supported date range. Do not speculate about the current date and do
            not repeatedly retry an invalid date. Format responses as Markdown in Chinese.
            """)
    @McpToolBox("weather")
    String chat(@UserMessage String question);
}

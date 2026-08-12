package com.samples.a2a;

import io.a2a.server.PublicAgentCard;
import io.a2a.spec.AgentCapabilities;
import io.a2a.spec.AgentCard;
import io.a2a.spec.AgentSkill;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.enterprise.inject.Produces;
import jakarta.inject.Inject;
import java.util.Collections;
import java.util.List;
import org.eclipse.microprofile.config.inject.ConfigProperty;

/**
 * Producer for weather agent card configuration.
 * This class is final and not designed for extension.
 */
@ApplicationScoped
public final class WeatherAgentCardProducer {

  /** The HTTP port for the agent service. */
  @Inject
  @ConfigProperty(name = "quarkus.http.port")
  private int httpPort;

  /**
   * Gets the HTTP port.
   *
   * @return the HTTP port
   */
  public int getHttpPort() {
    return httpPort;
  }

  /**
   * Produces the agent card for the weather agent.
   *
   * @return the configured agent card
   */
  @Produces
  @PublicAgentCard
  public AgentCard agentCard() {
    return new AgentCard.Builder()
        .name("Weather Agent")
        .description("Helps with China weather forecast and picking a good travel day")
        .url("http://localhost:" + getHttpPort())
        .version("1.0.0")
        .capabilities(
            new AgentCapabilities.Builder()
                .streaming(true)
                .pushNotifications(false)
                .stateTransitionHistory(false)
                .build())
        .defaultInputModes(Collections.singletonList("text"))
        .defaultOutputModes(Collections.singletonList("text"))
        .skills(
            Collections.singletonList(
                new AgentSkill.Builder()
                    .id("china_weather_search")
                    .name("Search China weather")
                    .description("Helps with daily weather forecasts for Chinese cities over a date range")
                    .tags(Collections.singletonList("china-weather"))
                    .examples(List.of("未来一周北京的天气怎么样", "8月20日到8月25日上海适合出行吗"))
                    .build()))
        .protocolVersion("0.3.0")
        .build();
  }
}

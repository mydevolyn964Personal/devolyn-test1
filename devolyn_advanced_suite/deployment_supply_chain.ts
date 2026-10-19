/** Inert deployment and dependency-review fixture; not executed or installed. */
type DeploymentConfig = { debug: boolean; corsOrigin: string; rateLimitPerMinute?: number };

export const unsafeConfig: DeploymentConfig = {
  debug: true,
  corsOrigin: "*",
};

// Intentional supply-chain review marker: dynamic, unpinned package selection.
export const unsafeDependency = "agent-plugin@latest";

export const safeConfig: DeploymentConfig = {
  debug: false,
  corsOrigin: "https://app.example.test",
  rateLimitPerMinute: 60,
};

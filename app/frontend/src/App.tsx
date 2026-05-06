import { useEffect, useState } from "react";

type Summary = {
  high: number;
  medium: number;
  low: number;
  info: number;
  total_servers: number;
  total_findings: number;
};

type Server = {
  hostname: string;
  role: string;
  os: { name: string; version: string };
  middleware: Array<{ name: string; version: string }>;
  runtimes: Array<{ name: string; version: string }>;
};

type Finding = {
  level: string;
  server: string;
  component_type: string;
  component_name: string;
  version: string;
  eol_date: string;
  days_to_eol: number;
  summary: string;
  recommendation: string;
};

type ScanResult = {
  generated_at: string;
  inventory: {
    service_name: string;
    environment: string;
    owner: string;
    servers: Server[];
  };
  summary: Summary;
  findings: Finding[];
};

const API_BASE = import.meta.env.VITE_API_BASE ?? "http://localhost:8000";

export default function App() {
  const [inventoryText, setInventoryText] = useState("");
  const [result, setResult] = useState<ScanResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    void loadSampleInventory();
  }, []);

  async function loadSampleInventory() {
    const response = await fetch("/sample-inventory.yml");
    const text = await response.text();
    setInventoryText(text);
  }

  async function runScan() {
    setLoading(true);
    setError("");
    try {
      const response = await fetch(`${API_BASE}/scan`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ inventory_text: inventoryText }),
      });
      if (!response.ok) {
        throw new Error(`scan に失敗しました。HTTP status: ${response.status}`);
      }
      const payload = (await response.json()) as ScanResult;
      setResult(payload);
    } catch (scanError) {
      setError(scanError instanceof Error ? scanError.message : "不明なエラーが発生しました。");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="page">
      <section className="hero">
        <div className="eyebrow">Infrastructure Lifecycle Management</div>
        <h1>infra-lifecycle-portal</h1>
        <p className="lead">
          OS、middleware、runtime の EOL リスクを確認し、migration planning、verification scope、
          rollback 準備につなげるための dashboard です。
        </p>
      </section>

      <section className="panel">
        <div className="section-header">
          <div>
            <h2>Inventory 入力</h2>
            <p>sample inventory を読み込むか、確認したい YAML を貼り付けてください。</p>
          </div>
          <div className="actions">
            <button type="button" onClick={() => void loadSampleInventory()}>
              Sample 読み込み
            </button>
            <button type="button" onClick={() => void runScan()} disabled={loading}>
              {loading ? "Scan 中..." : "Scan 実行"}
            </button>
          </div>
        </div>
        <textarea
          value={inventoryText}
          onChange={(event) => setInventoryText(event.target.value)}
          className="editor"
        />
        {error ? <p className="error">{error}</p> : null}
      </section>

      {result ? (
        <>
          <section className="panel">
            <div className="section-header">
              <div>
                <h2>リスクサマリー</h2>
                <p>
                  {result.inventory.service_name} / {result.inventory.environment} / 生成日時{" "}
                  {result.generated_at}
                </p>
              </div>
            </div>
            <div className="summary-grid">
              <SummaryCard label="HIGH" value={result.summary.high} tone="high" />
              <SummaryCard label="MEDIUM" value={result.summary.medium} tone="medium" />
              <SummaryCard label="LOW" value={result.summary.low} tone="low" />
              <SummaryCard label="INFO" value={result.summary.info} tone="info" />
            </div>
          </section>

          <section className="panel">
            <div className="section-header">
              <div>
                <h2>サーバー一覧</h2>
                <p>現在の inventory には {result.summary.total_servers} 台の server が登録されています。</p>
              </div>
            </div>
            <div className="server-grid">
              {result.inventory.servers.map((server) => (
                <article className="server-card" key={server.hostname}>
                  <h3>{server.hostname}</h3>
                  <p>{server.role}</p>
                  <div className="mono">
                    <div>OS: {server.os.name} {server.os.version}</div>
                    <div>
                      Middleware:{" "}
                      {server.middleware.map((item) => `${item.name} ${item.version}`).join(", ") || "-"}
                    </div>
                    <div>
                      Runtimes:{" "}
                      {server.runtimes.map((item) => `${item.name} ${item.version}`).join(", ") || "-"}
                    </div>
                  </div>
                </article>
              ))}
            </div>
          </section>

          <section className="panel">
            <div className="section-header">
              <div>
                <h2>検出されたリスク</h2>
                <p>{result.summary.total_findings} 件の lifecycle finding を検出しました。</p>
              </div>
            </div>
            <div className="findings">
              {result.findings.map((finding, index) => (
                <article className={`finding finding-${finding.level.toLowerCase()}`} key={`${finding.server}-${index}`}>
                  <div className="finding-top">
                    <span className="badge">{finding.level}</span>
                    <span className="mono">
                      {finding.server} / {finding.component_type} / {finding.component_name} {finding.version}
                    </span>
                  </div>
                  <p>{finding.summary}</p>
                  <p className="muted">
                    EOL: {finding.eol_date} / EOL までの日数: {finding.days_to_eol}
                  </p>
                  <p className="muted">{finding.recommendation}</p>
                </article>
              ))}
            </div>
          </section>
        </>
      ) : null}
    </main>
  );
}

function SummaryCard({ label, value, tone }: { label: string; value: number; tone: string }) {
  return (
    <article className={`summary-card ${tone}`}>
      <div>{label}</div>
      <strong>{value}</strong>
    </article>
  );
}

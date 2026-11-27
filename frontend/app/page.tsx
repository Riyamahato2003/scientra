export const dynamic = "force-dynamic";

async function checkReadiness(): Promise<boolean> {
  const base = process.env.BACKEND_URL ?? "http://localhost:8000";
  try {
    const response = await fetch(base + "/health/ready", {
      cache: "no-store",
      signal: AbortSignal.timeout(5000),
    });
    if (!response.ok) return false;
    const result: unknown = await response.json();
    return (
      typeof result === "object" &&
      result !== null &&
      "status" in result &&
      "database" in result &&
      result.status === "ok" &&
      result.database === "ready"
    );
  } catch {
    return false;
  }
}

export default async function Home() {
  const ready = await checkReadiness();
  return (
    <main className="mx-auto max-w-2xl px-6 py-20">
      <p className="text-sm font-semibold uppercase tracking-widest">Checkpoint 01</p>
      <h1 className="mt-4 text-5xl font-semibold tracking-tight">Scientra</h1>
      <p className="mt-4 text-lg">Turning scientific intelligence into revenue.</p>
      <section className="mt-10 rounded-xl border border-slate-300 bg-white p-6">
        <h2 className="text-xl font-semibold">Foundation status</h2>
        <p className="mt-4" role="status">
          {ready ? "API and database connected" : "API or database unavailable"}
        </p>
        <p className="mt-4 text-sm text-slate-600">
          Development foundation only. No live scientific intelligence or customer data.
        </p>
      </section>
    </main>
  );
}

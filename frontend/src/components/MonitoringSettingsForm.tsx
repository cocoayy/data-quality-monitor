"use client";

import { useState } from "react";
import { patchMonitoringSettings } from "@/lib/api";

type Props = {
  datasetId: string;
  monitoringEnabled: boolean;
  excludedFromScoring: boolean;
  expectedUpdateCycle: string | null;
};

const cycles = ["daily", "weekly", "monthly", "quarterly", "yearly", "unknown"];

export function MonitoringSettingsForm({
  datasetId,
  monitoringEnabled,
  excludedFromScoring,
  expectedUpdateCycle,
}: Props) {
  const [enabled, setEnabled] = useState(monitoringEnabled);
  const [excluded, setExcluded] = useState(excludedFromScoring);
  const [cycle, setCycle] = useState(expectedUpdateCycle ?? "unknown");
  const [message, setMessage] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);

  const onSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setSaving(true);
    setMessage(null);

    try {
      await patchMonitoringSettings(datasetId, {
        monitoringEnabled: enabled,
        excludedFromScoring: excluded,
        expectedUpdateCycle: cycle,
      });

      setMessage("監視設定を更新しました。ページを再読み込みすると最新値が反映されます。");
    } catch {
      setMessage("更新に失敗しました。");
    } finally {
      setSaving(false);
    }
  };

  return (
    <form
      onSubmit={onSubmit}
      style={{
        border: "1px solid #ddd",
        borderRadius: 8,
        padding: 16,
        marginTop: 16,
        backgroundColor: "#fff",
      }}
    >
      <h3 style={{ marginTop: 0 }}>監視設定編集</h3>

      <label style={fieldStyle}>
        <span>監視有効</span>
        <input
          type="checkbox"
          checked={enabled}
          onChange={(e) => setEnabled(e.target.checked)}
        />
      </label>

      <label style={fieldStyle}>
        <span>スコア除外</span>
        <input
          type="checkbox"
          checked={excluded}
          onChange={(e) => setExcluded(e.target.checked)}
        />
      </label>

      <label style={fieldStyle}>
        <span>更新周期</span>
        <select value={cycle} onChange={(e) => setCycle(e.target.value)}>
          {cycles.map((item) => (
            <option key={item} value={item}>
              {item}
            </option>
          ))}
        </select>
      </label>

      <button type="submit" disabled={saving} style={{ marginTop: 12 }}>
        {saving ? "保存中..." : "保存"}
      </button>

      {message && <p style={{ marginTop: 12 }}>{message}</p>}
    </form>
  );
}

const fieldStyle: React.CSSProperties = {
  display: "flex",
  justifyContent: "space-between",
  alignItems: "center",
  gap: 12,
  marginTop: 12,
};
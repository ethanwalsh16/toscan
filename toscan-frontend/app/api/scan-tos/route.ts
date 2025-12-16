import { NextRequest, NextResponse } from "next/server";

const BACKEND_URL = "http://localhost:5000/scan-tos";

export async function POST(req: NextRequest) {
  try {
    const payload = await req.json();

    const upstream = await fetch(BACKEND_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    const data = await upstream.json().catch(() => ({}));
    return NextResponse.json(data, { status: upstream.status });
  } catch (err) {
    console.error("scan-tos proxy error:", err);
    return NextResponse.json(
      { error: "Failed to forward request to backend" },
      { status: 502 }
    );
  }
}
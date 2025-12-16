"use client";

import React, { useState } from "react";

export default function Input() {

  const [tos, setTos] = useState("");
  const [company, setCompany] = useState("");
  const [date, setDate] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<any>(null);

  const handleSubmit = async (e: React.FormEvent) => {
	e.preventDefault();
	try {
		const res = await fetch("/api/scan-tos", {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({
				body: tos,
				company,
				date,
			}),
		});
		const data = await res.json();
		if(!res.ok) {
			setError(data?.error || "Request failed");
		} else {
			setResult(data);
		}
	} catch (err) {
		setError("An unexpected error occurred");
	} finally {
		setLoading(false);
	}
  };

 return (
    <div className="w-[50%] min-h-32 mx-auto mt-16 border border-zinc-500 rounded-xl p-8">
      <form onSubmit={handleSubmit}>
        <p className="pb-3">Terms of Service:</p>
        <textarea
          className="w-full h-48 p-4 bg-transparent border border-zinc-500 rounded-xl resize-y focus:outline-none focus:ring-0"
          placeholder="paste tos here"
          value={tos}
          onChange={(e) => setTos(e.target.value)}
        ></textarea>
        <h2 className="py-3">Optionally, include these additional fields.</h2>

        <div className="flex items-center space-x-4 mb-3">
          <label className="w-36 text-sm font-medium">Company Name:</label>
          <input
            className="flex-1 bg-transparent border border-zinc-500 rounded-md px-3 py-2 focus:outline-none focus:ring-0"
            placeholder="enter company here"
            value={company}
            onChange={(e) => setCompany(e.target.value)}
          />
        </div>
        <div className="flex items-center space-x-4">
          <label className="w-36 text-sm font-medium">Date of TOS retrieval:</label>
          <input
            className="flex-1 bg-transparent border border-zinc-500 rounded-md px-3 py-2 focus:outline-none focus:ring-0"
            type="date"
            value={date}
            onChange={(e) => setDate(e.target.value)}
          />
          <button
            type="submit"
            className="ml-4 px-4 py-2 bg-blue-600 text-white rounded-md cursor-pointer disabled:opacity-60"
            disabled={loading}
          >
            {loading ? "Scanning..." : "Scan TOS"}
          </button>
        </div>
      </form>

	     {/* Simple result/error display */}
      <div className="mt-4 text-sm">
        {error && <p className="text-red-500">Error: {error}</p>}
        {result && (
          <pre className="mt-2 whitespace-pre-wrap break-words border border-zinc-500 rounded-md p-3">
            {JSON.stringify(result, null, 2)}
          </pre>
        )}
      </div>
    </div>
  );
}	
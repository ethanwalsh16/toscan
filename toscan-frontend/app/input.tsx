export default function Input() {
  return (
	<div className="w-[50%] min-h-32 mx-auto mt-16 border border-zinc-500 rounded-xl p-8">
		
		<p className="pb-3">Terms of Service:</p>
		<textarea
			className="w-full h-48 p-4 bg-transparent border border-zinc-500 rounded-xl resize-y focus:outline-none focus:ring-0"
			placeholder="paste tos here"
		></textarea>
		<h2 className="py-3">Optionally, include these additional fields.</h2>

		<div className="flex items-center space-x-4 mb-3">
			<label className="w-36 text-sm font-medium">Company Name:</label>
			<input
				className="flex-1 bg-transparent border border-zinc-500 rounded-md px-3 py-2 focus:outline-none focus:ring-0"
				placeholder="enter company here"
			/>
		</div>

		<div className="flex items-center space-x-4">
			<label className="w-36 text-sm font-medium">Date of TOS retrieval:</label>
			<input
				className="flex-1 bg-transparent border border-zinc-500 rounded-md px-3 py-2 focus:outline-none focus:ring-0"
				type="date"
			/>
		</div>
	</div>
  );
}	
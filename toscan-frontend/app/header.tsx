export default function Header() {
  return (
	<div className="flex items-center justify-between pt-4 pb-2 px-8 border-b border-zinc-50 w-full">
		<a href="/" className="text-4xl font-bold"><i>toscan</i></a>
		<div className="flex space-x-16">
			<a href="/" className="leading-none text-zinc-200 hover:text-zinc-300">Home</a>
			<a href="/explanation" className="leading-none text-zinc-200 hover:text-zinc-300">Explanation</a>
			<a href="/about" className="leading-none text-zinc-200 hover:text-zinc-300">About</a>	
		</div>
	</div>
  );
}
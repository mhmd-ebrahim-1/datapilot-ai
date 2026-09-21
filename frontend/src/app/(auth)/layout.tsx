export default function AuthLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="flex min-h-screen">
      <div className="hidden lg:flex flex-col justify-center items-center w-1/2 bg-slate-900 text-white p-12">
        <div className="max-w-md space-y-6">
          <h1 className="text-4xl font-bold">DataPilot AI</h1>
          <p className="text-lg text-slate-300">
            Turn your raw data into actionable insights instantly. Join thousands of data-driven teams.
          </p>
        </div>
      </div>
      <div className="flex flex-col justify-center items-center w-full lg:w-1/2 p-8">
        {children}
      </div>
    </div>
  );
}

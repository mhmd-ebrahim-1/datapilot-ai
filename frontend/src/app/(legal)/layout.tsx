export default function LegalLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="flex flex-col min-h-screen">
      <header className="px-4 lg:px-6 h-14 flex items-center border-b shadow-sm">
        <a className="flex items-center justify-center font-bold text-xl text-primary" href="/">
          DataPilot AI
        </a>
      </header>
      <main className="flex-1 py-12 px-4 md:px-6 max-w-4xl mx-auto w-full">
        {children}
      </main>
      <footer className="border-t py-6 text-center text-sm text-muted-foreground">
        © 2024 DataPilot AI. All rights reserved.
      </footer>
    </div>
  );
}

export default function PrivacyPolicyPage() {
  return (
    <div className="space-y-8 prose prose-slate max-w-none dark:prose-invert">
      <h1 className="text-3xl font-bold tracking-tight">Privacy Policy</h1>
      <p className="text-muted-foreground">Last updated: October 24, 2024</p>
      
      <section>
        <h2 className="text-xl font-semibold mt-8 mb-4">1. Introduction</h2>
        <p>Welcome to DataPilot AI. We respect your privacy and are committed to protecting your personal data.</p>
      </section>

      <section>
        <h2 className="text-xl font-semibold mt-8 mb-4">2. Data We Collect</h2>
        <p>We collect information you provide directly to us when you create an account, upload datasets, or communicate with our support team.</p>
        <ul className="list-disc pl-6 mt-2 space-y-1">
          <li>Account information (name, email)</li>
          <li>Uploaded datasets and files</li>
          <li>Usage data and chat history</li>
        </ul>
      </section>

      <section>
        <h2 className="text-xl font-semibold mt-8 mb-4">3. Data Security</h2>
        <p>We implement appropriate technical and organizational measures to ensure a level of security appropriate to the risk, including encryption of data in transit and at rest.</p>
      </section>
    </div>
  )
}

import type { Metadata } from "next";
import { Inter } from "next/font/google";
import { QueryProvider } from "@/components/providers/query-provider";
import { Toaster } from "@/components/ui/toaster";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  metadataBase: new URL(process.env.NEXT_PUBLIC_APP_URL || "https://datapilot.ai"),
  title: "DataPilot AI — Turn Your Data Into Decisions",
  description: "AI-Powered Business Intelligence SaaS platform that turns raw Excel & CSV datasets into actionable KPIs, interactive charts, executive PDF reports, and AI explanations.",
  keywords: ["business intelligence", "AI analytics", "data cleaning", "automated KPIs", "executive reports", "data forecasting", "anomaly detection"],
  authors: [{ name: "DataPilot AI Team" }],
  icons: {
    icon: "/icon.svg",
    shortcut: "/icon.svg",
    apple: "/icon.svg",
  },
  openGraph: {
    title: "DataPilot AI — Turn Your Data Into Decisions",
    description: "Automated business intelligence, data profiling, KPI computation, and executive PDF reporting.",
    url: "https://datapilot.ai",
    siteName: "DataPilot AI",
    images: [
      {
        url: "/icon.svg",
        width: 800,
        height: 600,
        alt: "DataPilot AI Logo",
      },
    ],
    locale: "en_US",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "DataPilot AI — Turn Your Data Into Decisions",
    description: "Turn raw spreadsheets into interactive dashboards and executive PDF reports with AI.",
    images: ["/icon.svg"],
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <QueryProvider>
          {children}
          <Toaster />
        </QueryProvider>
      </body>
    </html>
  );
}

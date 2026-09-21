"use client"

import Link from "next/link";
import { 
  BarChart3, 
  Brain, 
  LayoutDashboard, 
  MessageSquare, 
  TrendingUp, 
  AlertTriangle, 
  FileText, 
  Users, 
  Check, 
  ArrowRight, 
  Sparkles, 
  ShieldCheck, 
  Zap, 
  Database
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

export default function Home() {
  const features = [
    {
      icon: BarChart3,
      title: "Smart Data Profiling",
      description: "Automatic type inference, missing value detection, distribution analysis, and data quality scoring from 0 to 100."
    },
    {
      icon: Brain,
      title: "AI-Powered Business Insights",
      description: "Generates high-impact observations, risks, and actionable growth recommendations grounded strictly in computed metrics."
    },
    {
      icon: LayoutDashboard,
      title: "Interactive Dashboards",
      description: "Auto-generates tailor-made charts, revenue curves, and KPI scorecards matching your exact dataset category."
    },
    {
      icon: MessageSquare,
      title: "Natural-Language Data Chat",
      description: "Ask questions like 'Which product had the highest profit in Q3?' and receive instant, deterministic answers."
    },
    {
      icon: TrendingUp,
      title: "Statistical Forecasting",
      description: "Accurately project trends, revenue, and demand with customizable horizons and confidence intervals."
    },
    {
      icon: AlertTriangle,
      title: "Outlier & Anomaly Detection",
      description: "Statistical IQR and Z-score outlier detection flags unusual spikes, drops, or data anomalies automatically."
    },
    {
      icon: FileText,
      title: "Executive PDF Reports",
      description: "Export high-resolution, branded executive summaries with KPI tables, charts, and recommendations in one click."
    },
    {
      icon: Users,
      title: "Team Workspaces",
      description: "Multi-tenant collaboration with role-based access control (Owner, Admin, Analyst, Viewer) and shared analytics."
    }
  ];

  const pricingPlans = [
    {
      name: "Free",
      price: "$0",
      period: "forever",
      description: "Essential automated analysis for individuals and small files.",
      popular: false,
      features: [
        "Up to 5 Datasets",
        "10 Analyses per month",
        "500 MB Secure Storage",
        "Automated Data Cleaning",
        "Basic Data Quality Reports",
        "Standard Visualizations"
      ],
      cta: "Get Started Free",
      href: "/register"
    },
    {
      name: "Pro",
      price: "$29",
      period: "/ month",
      description: "Advanced AI analytics, forecasting, and PDF reports for growing teams.",
      popular: true,
      features: [
        "Up to 50 Datasets",
        "100 Analyses per month",
        "5 GB Cloud Storage",
        "AI Business Insights & Recommendations",
        "Conversational Natural Language Chat",
        "Time-Series Trend Forecasting",
        "Statistical Anomaly Detection",
        "Executive PDF Report Export"
      ],
      cta: "Start 14-Day Free Trial",
      href: "/register"
    },
    {
      name: "Business",
      price: "$99",
      period: "/ month",
      description: "Maximum scale, team workspaces, and enterprise-grade data intelligence.",
      popular: false,
      features: [
        "Up to 500 Datasets",
        "1,000 Analyses per month",
        "50 GB Storage",
        "Multi-User Team Workspaces",
        "Custom Branding & White-Label Reports",
        "Unlimited AI Data Chat",
        "Priority Background Processing",
        "Dedicated Support & Audit Logging"
      ],
      cta: "Scale Your Business",
      href: "/register"
    }
  ];

  const faqs = [
    {
      q: "What file formats does DataPilot AI support?",
      a: "DataPilot supports CSV files (.csv) and Microsoft Excel workbooks (.xlsx, .xls) up to 50MB per file with automatic delimiter and encoding detection."
    },
    {
      q: "How does DataPilot prevent AI hallucinations?",
      a: "DataPilot never feeds raw, unfiltered datasets directly to large language models. Our Python analytics engine first calculates verified mathematical facts using Pandas and scikit-learn. The AI is only used to explain verified metrics in clear executive language."
    },
    {
      q: "Is my business data secure and confidential?",
      a: "Yes. Data is isolated strictly by workspace with UUID access control. We never use your proprietary data to train foundation models."
    },
    {
      q: "Can I download and share reports with my clients?",
      a: "Absolutely. You can generate publication-ready PDF reports complete with KPI cards, data quality assessments, and strategic insights."
    }
  ];

  return (
    <div className="flex flex-col min-h-screen bg-background text-foreground selection:bg-indigo-500 selection:text-white">
      {/* 1. Header / Navbar */}
      <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <Link className="flex items-center gap-2 font-bold text-xl tracking-tight text-indigo-600 dark:text-indigo-400" href="/">
            <div className="h-8 w-8 rounded-lg bg-indigo-600 text-white flex items-center justify-center font-black">
              DP
            </div>
            DataPilot AI
          </Link>
          <nav className="hidden md:flex items-center gap-8 text-sm font-medium text-muted-foreground">
            <Link className="hover:text-foreground transition-colors" href="#features">Features</Link>
            <Link className="hover:text-foreground transition-colors" href="#how-it-works">How It Works</Link>
            <Link className="hover:text-foreground transition-colors" href="#pricing">Pricing</Link>
            <Link className="hover:text-foreground transition-colors" href="#faq">FAQ</Link>
          </nav>
          <div className="flex items-center gap-3">
            <Link href="/login">
              <Button variant="ghost" size="sm">Sign In</Button>
            </Link>
            <Link href="/register">
              <Button size="sm" className="bg-indigo-600 hover:bg-indigo-700 text-white shadow-sm">
                Get Started <ArrowRight className="ml-1.5 h-3.5 w-3.5" />
              </Button>
            </Link>
          </div>
        </div>
      </header>

      <main className="flex-1">
        {/* 2. Hero Section */}
        <section className="relative overflow-hidden pt-20 pb-28 md:pt-28 md:pb-36 bg-gradient-to-b from-indigo-50/50 via-background to-background dark:from-indigo-950/20">
          <div className="container mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-semibold bg-indigo-100 text-indigo-800 dark:bg-indigo-900/50 dark:text-indigo-300 mb-6 animate-pulse">
              <Sparkles className="h-3.5 w-3.5" /> Next-Gen AI Business Intelligence Engine
            </div>
            <h1 className="text-4xl sm:text-5xl md:text-6xl font-extrabold tracking-tight text-slate-900 dark:text-white max-w-4xl mx-auto leading-tight">
              Turn Your Data Into <span className="bg-gradient-to-r from-indigo-600 to-violet-600 bg-clip-text text-transparent">Decisions.</span>
            </h1>
            <p className="mt-6 text-lg sm:text-xl text-muted-foreground max-w-2xl mx-auto leading-relaxed">
              Upload your Excel or CSV datasets. DataPilot cleans your data, calculates KPIs, predicts trends, surfaces anomalies, and writes executive PDF reports in seconds.
            </p>
            <div className="mt-8 flex flex-col sm:flex-row items-center justify-center gap-4">
              <Link href="/register">
                <Button size="lg" className="w-full sm:w-auto h-12 px-8 bg-indigo-600 hover:bg-indigo-700 text-white text-base shadow-lg shadow-indigo-500/25">
                  Start Free Analysis <ArrowRight className="ml-2 h-4 w-4" />
                </Button>
              </Link>
              <Link href="#features">
                <Button variant="outline" size="lg" className="w-full sm:w-auto h-12 px-8 text-base">
                  Explore Features
                </Button>
              </Link>
            </div>

            {/* Dashboard Mockup Preview */}
            <div className="mt-16 max-w-5xl mx-auto rounded-xl border bg-card text-card-foreground shadow-2xl overflow-hidden">
              <div className="border-b bg-muted/40 px-4 py-3 flex items-center gap-2">
                <div className="flex gap-1.5">
                  <div className="h-3 w-3 rounded-full bg-red-400" />
                  <div className="h-3 w-3 rounded-full bg-amber-400" />
                  <div className="h-3 w-3 rounded-full bg-emerald-400" />
                </div>
                <div className="text-xs text-muted-foreground font-mono ml-2">datapilot.ai/dashboard/datasets/sales-2024</div>
              </div>
              <div className="p-6 md:p-8 bg-slate-950 text-white grid grid-cols-1 md:grid-cols-4 gap-4 text-left">
                <div className="p-4 rounded-lg bg-slate-900 border border-slate-800">
                  <p className="text-xs text-slate-400">Total Revenue</p>
                  <p className="text-2xl font-bold mt-1 text-emerald-400">$1,428,500.00</p>
                  <span className="text-xs text-emerald-500">↑ +18.4% vs last period</span>
                </div>
                <div className="p-4 rounded-lg bg-slate-900 border border-slate-800">
                  <p className="text-xs text-slate-400">Data Quality Score</p>
                  <p className="text-2xl font-bold mt-1 text-indigo-400">98.4 / 100</p>
                  <span className="text-xs text-slate-400">0 duplicate rows removed</span>
                </div>
                <div className="p-4 rounded-lg bg-slate-900 border border-slate-800">
                  <p className="text-xs text-slate-400">Projected Growth</p>
                  <p className="text-2xl font-bold mt-1 text-purple-400">+24.8%</p>
                  <span className="text-xs text-purple-400">30-day SMA model</span>
                </div>
                <div className="p-4 rounded-lg bg-slate-900 border border-slate-800">
                  <p className="text-xs text-slate-400">Anomalies Detected</p>
                  <p className="text-2xl font-bold mt-1 text-amber-400">2 flagged</p>
                  <span className="text-xs text-amber-400">Statistical IQR range</span>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* 3. How It Works Section */}
        <section id="how-it-works" className="py-20 bg-muted/30 border-y">
          <div className="container mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <h2 className="text-3xl font-bold tracking-tight">How DataPilot Works</h2>
            <p className="mt-2 text-muted-foreground max-w-xl mx-auto">From messy spreadsheets to executive decisions in four automated steps.</p>
            <div className="mt-12 grid grid-cols-1 md:grid-cols-4 gap-8">
              {[
                { step: "01", title: "Upload Dataset", desc: "Drop your CSV or Excel file. Our ingestion validator verifies headers and size safely." },
                { step: "02", title: "Automated Cleaning", desc: "Whitespace is trimmed, nulls standardized, and duplicate records cleansed." },
                { step: "03", title: "Metrics & Forecasting", desc: "Deterministic KPIs, correlation matrix, charts, and forecasts are generated." },
                { step: "04", title: "Decide & Export", desc: "Chat with your data, review strategic insights, and download executive PDF reports." }
              ].map((item, i) => (
                <div key={i} className="relative flex flex-col items-center p-6 bg-card rounded-xl border shadow-sm text-center">
                  <div className="h-10 w-10 rounded-full bg-indigo-600 text-white flex items-center justify-center font-bold text-sm mb-4">
                    {item.step}
                  </div>
                  <h3 className="font-semibold text-lg">{item.title}</h3>
                  <p className="mt-2 text-sm text-muted-foreground">{item.desc}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* 4. Features Grid */}
        <section id="features" className="py-24">
          <div className="container mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center max-w-3xl mx-auto">
              <Badge variant="outline" className="mb-3 border-indigo-200 text-indigo-700 dark:text-indigo-300">Complete BI Capabilities</Badge>
              <h2 className="text-3xl sm:text-4xl font-bold tracking-tight">Everything You Need To Master Your Data</h2>
              <p className="mt-3 text-muted-foreground">Purpose-built for executives, data analysts, marketers, and founders.</p>
            </div>
            <div className="mt-16 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              {features.map((f, i) => {
                const Icon = f.icon;
                return (
                  <Card key={i} className="transition-all hover:shadow-md hover:border-indigo-200 dark:hover:border-indigo-800">
                    <CardHeader className="pb-3">
                      <div className="h-10 w-10 rounded-lg bg-indigo-50 dark:bg-indigo-950/50 text-indigo-600 dark:text-indigo-400 flex items-center justify-center mb-2">
                        <Icon className="h-5 w-5" />
                      </div>
                      <CardTitle className="text-lg">{f.title}</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <p className="text-sm text-muted-foreground">{f.description}</p>
                    </CardContent>
                  </Card>
                );
              })}
            </div>
          </div>
        </section>

        {/* 5. Pricing Table */}
        <section id="pricing" className="py-24 bg-muted/20 border-t">
          <div className="container mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center max-w-2xl mx-auto">
              <Badge variant="outline" className="mb-3 border-indigo-200 text-indigo-700 dark:text-indigo-300">Simple, Transparent Pricing</Badge>
              <h2 className="text-3xl sm:text-4xl font-bold tracking-tight">Choose The Plan That Fits Your Scale</h2>
              <p className="mt-3 text-muted-foreground">Upgrade, downgrade, or cancel anytime.</p>
            </div>
            <div className="mt-16 grid grid-cols-1 lg:grid-cols-3 gap-8 max-w-6xl mx-auto">
              {pricingPlans.map((plan, i) => (
                <Card key={i} className={`flex flex-col justify-between relative ${plan.popular ? 'border-2 border-indigo-600 shadow-xl' : 'shadow-sm'}`}>
                  {plan.popular && (
                    <div className="absolute -top-3.5 left-1/2 -translate-x-1/2 px-3 py-1 bg-indigo-600 text-white text-xs font-bold rounded-full uppercase tracking-wider">
                      Most Popular
                    </div>
                  )}
                  <CardHeader>
                    <CardTitle className="text-2xl">{plan.name}</CardTitle>
                    <CardDescription className="min-h-[40px] mt-1">{plan.description}</CardDescription>
                    <div className="mt-4 flex items-baseline">
                      <span className="text-4xl font-extrabold tracking-tight">{plan.price}</span>
                      <span className="ml-1 text-sm text-muted-foreground">{plan.period}</span>
                    </div>
                  </CardHeader>
                  <CardContent className="flex-1">
                    <ul className="space-y-3 text-sm">
                      {plan.features.map((feat, fi) => (
                        <li key={fi} className="flex items-center gap-2">
                          <Check className="h-4 w-4 text-emerald-500 shrink-0" />
                          <span>{feat}</span>
                        </li>
                      ))}
                    </ul>
                  </CardContent>
                  <CardFooter className="pt-4">
                    <Link href={plan.href} className="w-full">
                      <Button className={`w-full ${plan.popular ? 'bg-indigo-600 hover:bg-indigo-700 text-white' : ''}`} variant={plan.popular ? 'default' : 'outline'}>
                        {plan.cta}
                      </Button>
                    </Link>
                  </CardFooter>
                </Card>
              ))}
            </div>
          </div>
        </section>

        {/* 6. FAQ Section */}
        <section id="faq" className="py-24 border-t">
          <div className="container mx-auto px-4 sm:px-6 lg:px-8 max-w-4xl">
            <div className="text-center mb-16">
              <h2 className="text-3xl font-bold tracking-tight">Frequently Asked Questions</h2>
              <p className="mt-2 text-muted-foreground">Everything you need to know about the product and privacy.</p>
            </div>
            <div className="space-y-6">
              {faqs.map((faq, i) => (
                <div key={i} className="p-6 rounded-xl border bg-card">
                  <h3 className="text-base font-semibold text-foreground">{faq.q}</h3>
                  <p className="mt-2 text-sm text-muted-foreground leading-relaxed">{faq.a}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* 7. Call To Action Banner */}
        <section className="py-20 bg-indigo-600 text-white text-center">
          <div className="container mx-auto px-4 sm:px-6 lg:px-8 max-w-3xl">
            <h2 className="text-3xl sm:text-4xl font-extrabold tracking-tight">Ready To Transform Your Raw Data?</h2>
            <p className="mt-4 text-indigo-100 text-lg">
              Join data-driven teams using DataPilot AI to automate reports, unlock insights, and make faster business decisions.
            </p>
            <div className="mt-8 flex justify-center">
              <Link href="/register">
                <Button size="lg" className="h-12 px-8 bg-white text-indigo-600 hover:bg-slate-100 font-semibold shadow-lg">
                  Create Your Free Account <ArrowRight className="ml-2 h-4 w-4" />
                </Button>
              </Link>
            </div>
          </div>
        </section>
      </main>

      {/* 8. Footer */}
      <footer className="border-t bg-muted/40 py-12 text-sm text-muted-foreground">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row justify-between items-center gap-6">
          <div className="flex items-center gap-2">
            <div className="h-6 w-6 rounded bg-indigo-600 text-white flex items-center justify-center font-bold text-xs">DP</div>
            <span className="font-semibold text-foreground">DataPilot AI</span>
            <span className="text-xs">© 2024 DataPilot AI. All rights reserved.</span>
          </div>
          <div className="flex gap-6">
            <Link className="hover:text-foreground transition-colors" href="/privacy">Privacy Policy</Link>
            <Link className="hover:text-foreground transition-colors" href="/terms">Terms of Service</Link>
          </div>
        </div>
      </footer>
    </div>
  );
}

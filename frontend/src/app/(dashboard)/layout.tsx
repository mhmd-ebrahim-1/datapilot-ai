"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { LayoutDashboard, Database, FileText, MessageSquare, Settings, Users, LogOut } from "lucide-react";
import { useAuthStore } from "@/lib/auth";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const router = useRouter();
  const { isAuthenticated, user, logout } = useAuthStore();

  useEffect(() => {
    if (!isAuthenticated) {
      router.push("/login");
    }
  }, [isAuthenticated, router]);

  if (!isAuthenticated) return null;

  return (
    <div className="flex h-screen overflow-hidden bg-gray-100 dark:bg-slate-900">
      {/* Sidebar */}
      <aside className="w-64 bg-white dark:bg-slate-950 border-r flex flex-col hidden md:flex">
        <div className="h-14 flex items-center px-4 border-b">
          <span className="font-bold text-lg text-primary">DataPilot AI</span>
        </div>
        
        <div className="flex-1 overflow-y-auto py-4">
          <nav className="space-y-1 px-2">
            <NavItem href="/dashboard" icon={LayoutDashboard} label="Dashboard" />
            <NavItem href="/datasets" icon={Database} label="Datasets" />
            <NavItem href="/reports" icon={FileText} label="Reports" />
            <NavItem href="/chat" icon={MessageSquare} label="AI Chat" />
          </nav>
        </div>

        <div className="p-4 border-t space-y-2">
          <NavItem href="/settings" icon={Settings} label="Settings" />
          <NavItem href="/admin" icon={Users} label="Admin" />
          <button 
            onClick={() => { logout(); router.push("/login"); }}
            className="flex items-center w-full px-2 py-2 text-sm font-medium rounded-md text-red-600 hover:bg-red-50"
          >
            <LogOut className="mr-3 h-5 w-5" />
            Logout
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col overflow-hidden">
        <header className="h-14 bg-white dark:bg-slate-950 border-b flex items-center justify-between px-4">
          <div className="font-medium text-sm">Welcome back, {user?.name}</div>
          <div className="flex items-center space-x-4">
            <div className="h-8 w-8 rounded-full bg-primary text-white flex items-center justify-center font-bold">
              {user?.name?.[0]?.toUpperCase()}
            </div>
          </div>
        </header>
        <div className="flex-1 overflow-auto p-4 md:p-6 lg:p-8">
          {children}
        </div>
      </main>
    </div>
  );
}

function NavItem({ href, icon: Icon, label }: { href: string; icon: any; label: string }) {
  return (
    <Link
      href={href}
      className="flex items-center px-2 py-2 text-sm font-medium rounded-md text-slate-700 hover:bg-slate-100 dark:text-slate-300 dark:hover:bg-slate-800"
    >
      <Icon className="mr-3 h-5 w-5 text-slate-500" />
      {label}
    </Link>
  );
}

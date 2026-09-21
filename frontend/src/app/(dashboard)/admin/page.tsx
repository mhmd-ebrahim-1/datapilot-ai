"use client";

import { useQuery } from "@tanstack/react-query";
import { PageHeader } from "@/components/common/page-header";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Users, Database, Building2, CreditCard, ShieldAlert, Loader2 } from "lucide-react";
import { useAuthStore } from "@/lib/auth";
import { api } from "@/lib/api";

export default function AdminPage() {
  const { user } = useAuthStore();

  const { data: stats, isLoading: statsLoading } = useQuery({
    queryKey: ["admin-stats"],
    queryFn: () => api.get<any>("/api/v1/admin/stats").catch(() => null)
  });

  const { data: users, isLoading: usersLoading } = useQuery({
    queryKey: ["admin-users"],
    queryFn: () => api.get<any[]>("/api/v1/admin/users").catch(() => [])
  });

  if (user && user.role !== "admin" && user.role !== "superadmin") {
    return (
      <div className="py-20 text-center space-y-4">
        <ShieldAlert className="h-12 w-12 text-destructive mx-auto" />
        <h2 className="text-2xl font-bold">Access Restricted</h2>
        <p className="text-muted-foreground max-w-md mx-auto text-sm">
          You need administrator privileges to view system metrics and user governance.
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <PageHeader 
        title="Superadmin Dashboard" 
        description="Global platform telemetry, aggregate user records, and workspace governance." 
      />
      
      {/* Platform Stats Grid */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <AdminStatCard 
          title="Total Users" 
          value={stats?.total_users?.toLocaleString() || "0"} 
          icon={Users} 
          trend="Registered SaaS accounts" 
        />
        <AdminStatCard 
          title="Active Workspaces" 
          value={stats?.total_workspaces?.toLocaleString() || "0"} 
          icon={Building2} 
          trend="Multi-tenant environments" 
        />
        <AdminStatCard 
          title="Total Datasets" 
          value={stats?.total_datasets?.toLocaleString() || "0"} 
          icon={Database} 
          trend="Uploaded files & sheets" 
        />
        <AdminStatCard 
          title="Active Subscriptions" 
          value={stats?.active_subscriptions?.toLocaleString() || "0"} 
          icon={CreditCard} 
          trend="Paid & trial tiers" 
        />
      </div>

      {/* Users Governance Table */}
      <Card>
        <CardHeader>
          <CardTitle>System Accounts</CardTitle>
          <CardDescription>Global registry of all platform users and permissions</CardDescription>
        </CardHeader>
        <CardContent>
          {usersLoading ? (
            <div className="py-12 text-center text-sm text-muted-foreground flex items-center justify-center gap-2">
              <Loader2 className="h-4 w-4 animate-spin text-indigo-600" />
              <span>Loading user database...</span>
            </div>
          ) : !users || users.length === 0 ? (
            <div className="py-12 text-center text-sm text-muted-foreground">No accounts found.</div>
          ) : (
            <div className="rounded-md border overflow-hidden">
              <Table>
                <TableHeader className="bg-muted/50">
                  <TableRow>
                    <TableHead>Name</TableHead>
                    <TableHead>Email</TableHead>
                    <TableHead>Role</TableHead>
                    <TableHead>Status</TableHead>
                    <TableHead>Created At</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {users.map((u: any) => (
                    <TableRow key={u.id} className="hover:bg-muted/30">
                      <TableCell className="font-semibold text-foreground">{u.name}</TableCell>
                      <TableCell className="text-muted-foreground">{u.email}</TableCell>
                      <TableCell>
                        <Badge variant="outline" className="capitalize text-xs font-semibold">
                          {u.role}
                        </Badge>
                      </TableCell>
                      <TableCell>
                        <Badge className={`text-[10px] ${u.is_active ? 'bg-emerald-600' : 'bg-destructive'}`}>
                          {u.is_active ? "Active" : "Disabled"}
                        </Badge>
                      </TableCell>
                      <TableCell className="text-xs text-muted-foreground">
                        {new Date(u.created_at).toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric' })}
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}

function AdminStatCard({ title, value, icon: Icon, trend }: any) {
  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium text-muted-foreground">{title}</CardTitle>
        <div className="h-8 w-8 rounded-lg bg-indigo-50 dark:bg-indigo-950 flex items-center justify-center text-indigo-600">
          <Icon className="h-4 w-4" />
        </div>
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold tracking-tight">{value}</div>
        <p className="text-xs text-muted-foreground mt-1">{trend}</p>
      </CardContent>
    </Card>
  );
}

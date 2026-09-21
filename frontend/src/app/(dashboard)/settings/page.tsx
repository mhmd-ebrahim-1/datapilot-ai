"use client";

import { useState, useEffect } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { PageHeader } from "@/components/common/page-header";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription, DialogFooter } from "@/components/ui/dialog";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Check, Shield, User as UserIcon, Building, CreditCard, Users, Zap, Trash2 } from "lucide-react";
import { useAuthStore } from "@/lib/auth";
import { useToast } from "@/components/ui/use-toast";
import { api } from "@/lib/api";

export default function SettingsPage() {
  const { user, fetchCurrentUser } = useAuthStore();
  const { toast } = useToast();
  const queryClient = useQueryClient();

  // Profile Form state
  const [name, setName] = useState(user?.name || "");
  const [isSavingProfile, setIsSavingProfile] = useState(false);

  // Invite modal state
  const [isInviteOpen, setIsInviteOpen] = useState(false);
  const [inviteEmail, setInviteEmail] = useState("");
  const [inviteRole, setInviteRole] = useState("analyst");

  // Fetch current user workspaces
  const { data: workspaces, isLoading: wsLoading } = useQuery({
    queryKey: ["workspaces-list"],
    queryFn: () => api.get<any[]>("/api/v1/workspaces")
  });

  const activeWorkspace = workspaces?.[0] || null;
  const workspaceId = activeWorkspace?.id;

  // Fetch workspace members
  const { data: members, isLoading: membersLoading } = useQuery({
    queryKey: ["workspace-members", workspaceId],
    queryFn: () => api.get<any[]>(`/api/v1/workspaces/${workspaceId}/members`),
    enabled: !!workspaceId
  });

  // Fetch billing & usage
  const { data: usageData, isLoading: usageLoading } = useQuery({
    queryKey: ["billing-usage"],
    queryFn: () => api.get<any>("/api/v1/billing/usage")
  });

  useEffect(() => {
    if (user?.name) setName(user.name);
  }, [user]);

  // Update Profile Mutation
  const handleSaveProfile = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSavingProfile(true);
    try {
      await api.put("/api/v1/auth/me", { name });
      await fetchCurrentUser();
      toast({ title: "Profile updated successfully!" });
    } catch (err: any) {
      toast({ title: "Failed to update profile", description: err.message, variant: "destructive" });
    } finally {
      setIsSavingProfile(false);
    }
  };

  // Upgrade Plan Mutation
  const upgradeMutation = useMutation({
    mutationFn: (plan: string) => api.post<any>("/api/v1/billing/upgrade", { plan }),
    onSuccess: (res) => {
      queryClient.invalidateQueries({ queryKey: ["billing-usage"] });
      toast({
        title: "Plan Upgraded!",
        description: res.message || "Your workspace limits have been increased."
      });
    },
    onError: (err: any) => {
      toast({ title: "Upgrade failed", description: err.message, variant: "destructive" });
    }
  });

  // Invite Member Mutation
  const inviteMutation = useMutation({
    mutationFn: (body: { email: string; role: string }) => 
      api.post<any>(`/api/v1/workspaces/${workspaceId}/members`, body),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["workspace-members", workspaceId] });
      setIsInviteOpen(false);
      setInviteEmail("");
      toast({ title: "Member invited to workspace" });
    },
    onError: (err: any) => {
      toast({ title: "Failed to invite member", description: err.message, variant: "destructive" });
    }
  });

  // Remove Member Mutation
  const removeMemberMutation = useMutation({
    mutationFn: (memberId: string) => api.delete(`/api/v1/workspaces/${workspaceId}/members/${memberId}`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["workspace-members", workspaceId] });
      toast({ title: "Member removed" });
    }
  });

  const currentPlan = usageData?.plan || "free";

  return (
    <div className="space-y-6 max-w-5xl">
      <PageHeader title="Settings & Workspace" description="Manage your user profile, active workspaces, team members, and subscription tier." />

      <Tabs defaultValue="profile" className="w-full">
        <TabsList className="mb-4 bg-muted/60 p-1">
          <TabsTrigger value="profile">Profile</TabsTrigger>
          <TabsTrigger value="workspace">Workspace</TabsTrigger>
          <TabsTrigger value="billing">Billing & Limits</TabsTrigger>
          <TabsTrigger value="members">Team Members</TabsTrigger>
        </TabsList>

        {/* 1. PROFILE TAB */}
        <TabsContent value="profile" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <UserIcon className="h-5 w-5 text-indigo-600" /> Personal Profile
              </CardTitle>
              <CardDescription>Update your personal display name and email address.</CardDescription>
            </CardHeader>
            <form onSubmit={handleSaveProfile}>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="name">Full Name</Label>
                  <Input id="name" value={name} onChange={(e) => setName(e.target.value)} required />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="email">Email Address</Label>
                  <Input id="email" type="email" value={user?.email || ""} disabled className="bg-muted cursor-not-allowed" />
                  <p className="text-xs text-muted-foreground">Contact support to change your account email.</p>
                </div>
                <div className="space-y-2">
                  <Label>System Role</Label>
                  <div>
                    <Badge variant="outline" className="capitalize">{user?.role || "User"}</Badge>
                  </div>
                </div>
              </CardContent>
              <CardFooter className="border-t pt-4">
                <Button type="submit" disabled={isSavingProfile} className="bg-indigo-600 hover:bg-indigo-700 text-white">
                  {isSavingProfile ? "Saving..." : "Save Profile Changes"}
                </Button>
              </CardFooter>
            </form>
          </Card>
        </TabsContent>

        {/* 2. WORKSPACE TAB */}
        <TabsContent value="workspace" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Building className="h-5 w-5 text-indigo-600" /> Active Workspace Configuration
              </CardTitle>
              <CardDescription>Organization branding and workspace settings.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label>Workspace Name</Label>
                <Input defaultValue={activeWorkspace?.name || "My Analytics Workspace"} />
              </div>
              <div className="space-y-2">
                <Label>Workspace ID</Label>
                <Input value={workspaceId || "Loading..."} disabled className="font-mono text-xs bg-muted" />
              </div>
              <div className="space-y-2">
                <Label>Your Role</Label>
                <div>
                  <Badge variant="outline" className="border-indigo-300 text-indigo-700 uppercase font-bold text-[10px]">
                    {activeWorkspace?.role || "Owner"}
                  </Badge>
                </div>
              </div>
            </CardContent>
            <CardFooter className="border-t pt-4">
              <Button className="bg-indigo-600 hover:bg-indigo-700 text-white">Update Workspace</Button>
            </CardFooter>
          </Card>
        </TabsContent>

        {/* 3. BILLING & LIMITS TAB */}
        <TabsContent value="billing" className="space-y-6">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between pb-4">
              <div>
                <CardTitle className="flex items-center gap-2">
                  <CreditCard className="h-5 w-5 text-indigo-600" /> Current Plan & Usage Limits
                </CardTitle>
                <CardDescription>Resource consumption for the current monthly billing period.</CardDescription>
              </div>
              <Badge className="bg-indigo-600 text-white uppercase text-xs px-3 py-1 font-bold">
                {currentPlan} Tier
              </Badge>
            </CardHeader>
            <CardContent className="space-y-6">
              {/* Usage metrics bars */}
              <div className="grid gap-4 sm:grid-cols-3">
                <div className="p-4 rounded-lg border bg-muted/30">
                  <div className="flex justify-between text-xs font-semibold mb-1">
                    <span>Uploaded Datasets</span>
                    <span>{usageData?.uploads?.used || 0} / {usageData?.uploads?.limit || 5}</span>
                  </div>
                  <div className="w-full h-2 rounded-full bg-muted overflow-hidden">
                    <div 
                      className="h-full bg-indigo-600" 
                      style={{ width: `${Math.min(100, ((usageData?.uploads?.used || 0) / Math.max(usageData?.uploads?.limit || 5, 1)) * 100)}%` }} 
                    />
                  </div>
                </div>

                <div className="p-4 rounded-lg border bg-muted/30">
                  <div className="flex justify-between text-xs font-semibold mb-1">
                    <span>Analyses Run</span>
                    <span>{usageData?.analyses?.used || 0} / {usageData?.analyses?.limit || 10}</span>
                  </div>
                  <div className="w-full h-2 rounded-full bg-muted overflow-hidden">
                    <div 
                      className="h-full bg-emerald-600" 
                      style={{ width: `${Math.min(100, ((usageData?.analyses?.used || 0) / Math.max(usageData?.analyses?.limit || 10, 1)) * 100)}%` }} 
                    />
                  </div>
                </div>

                <div className="p-4 rounded-lg border bg-muted/30">
                  <div className="flex justify-between text-xs font-semibold mb-1">
                    <span>AI Requests</span>
                    <span>{usageData?.ai_requests?.used || 0} / {usageData?.ai_requests?.limit || 20}</span>
                  </div>
                  <div className="w-full h-2 rounded-full bg-muted overflow-hidden">
                    <div 
                      className="h-full bg-purple-600" 
                      style={{ width: `${Math.min(100, ((usageData?.ai_requests?.used || 0) / Math.max(usageData?.ai_requests?.limit || 20, 1)) * 100)}%` }} 
                    />
                  </div>
                </div>
              </div>

              {/* Upgrade Plan Cards */}
              <div className="border-t pt-6">
                <h4 className="text-sm font-semibold mb-4">Upgrade Workspace Tier</h4>
                <div className="grid gap-4 sm:grid-cols-2">
                  <div className="p-4 rounded-lg border bg-card flex flex-col justify-between">
                    <div>
                      <div className="flex justify-between items-center mb-1">
                        <h5 className="font-bold text-base">Pro Plan</h5>
                        <span className="text-sm font-bold text-indigo-600">$29 / mo</span>
                      </div>
                      <p className="text-xs text-muted-foreground mb-3">50 datasets, 100 analyses, AI Chat, Forecasting & PDF Reports.</p>
                    </div>
                    <Button 
                      onClick={() => upgradeMutation.mutate("pro")}
                      disabled={currentPlan === "pro" || upgradeMutation.isPending}
                      variant={currentPlan === "pro" ? "outline" : "default"}
                      className="w-full bg-indigo-600 hover:bg-indigo-700 text-white text-xs"
                    >
                      {currentPlan === "pro" ? "Current Plan" : "Upgrade to Pro"}
                    </Button>
                  </div>

                  <div className="p-4 rounded-lg border bg-card flex flex-col justify-between">
                    <div>
                      <div className="flex justify-between items-center mb-1">
                        <h5 className="font-bold text-base">Business Plan</h5>
                        <span className="text-sm font-bold text-indigo-600">$99 / mo</span>
                      </div>
                      <p className="text-xs text-muted-foreground mb-3">500 datasets, 1,000 analyses, Team Workspaces & White-Labeling.</p>
                    </div>
                    <Button 
                      onClick={() => upgradeMutation.mutate("business")}
                      disabled={currentPlan === "business" || upgradeMutation.isPending}
                      variant={currentPlan === "business" ? "outline" : "default"}
                      className="w-full text-xs"
                    >
                      {currentPlan === "business" ? "Current Plan" : "Upgrade to Business"}
                    </Button>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* 4. MEMBERS TAB */}
        <TabsContent value="members" className="space-y-4">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between">
              <div>
                <CardTitle className="flex items-center gap-2">
                  <Users className="h-5 w-5 text-indigo-600" /> Workspace Team Members
                </CardTitle>
                <CardDescription>Collaborators who have access to this workspace.</CardDescription>
              </div>
              <Button onClick={() => setIsInviteOpen(true)} size="sm" className="bg-indigo-600 hover:bg-indigo-700 text-white">
                Invite Member
              </Button>
            </CardHeader>
            <CardContent>
              {membersLoading ? (
                <div className="py-8 text-center text-sm text-muted-foreground">Loading workspace members...</div>
              ) : !members || members.length === 0 ? (
                <div className="py-8 text-center text-sm text-muted-foreground">No collaborators added yet.</div>
              ) : (
                <div className="rounded-md border overflow-hidden">
                  <Table>
                    <TableHeader className="bg-muted/50">
                      <TableRow>
                        <TableHead>User</TableHead>
                        <TableHead>Email</TableHead>
                        <TableHead>Role</TableHead>
                        <TableHead className="text-right">Actions</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {members.map((m: any) => (
                        <TableRow key={m.id}>
                          <TableCell className="font-medium text-foreground">{m.name}</TableCell>
                          <TableCell className="text-muted-foreground">{m.email}</TableCell>
                          <TableCell>
                            <Badge variant="outline" className="capitalize text-xs">
                              {m.role}
                            </Badge>
                          </TableCell>
                          <TableCell className="text-right">
                            {m.role !== "owner" && (
                              <Button 
                                variant="ghost" 
                                size="sm" 
                                onClick={() => removeMemberMutation.mutate(m.id)}
                                className="text-destructive hover:bg-destructive/10"
                              >
                                <Trash2 className="h-3.5 w-3.5" />
                              </Button>
                            )}
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>

      {/* Invite Member Modal */}
      <Dialog open={isInviteOpen} onOpenChange={setIsInviteOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Invite Member to Workspace</DialogTitle>
            <DialogDescription>
              Invited members can view and collaborate on datasets and analyses within this workspace.
            </DialogDescription>
          </DialogHeader>
          <div className="space-y-4 py-2">
            <div className="space-y-2">
              <Label>Email Address</Label>
              <Input
                type="email"
                placeholder="colleague@company.com"
                value={inviteEmail}
                onChange={(e) => setInviteEmail(e.target.value)}
              />
            </div>
            <div className="space-y-2">
              <Label>Workspace Role</Label>
              <Select value={inviteRole} onValueChange={setInviteRole}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="analyst">Analyst (Can upload & run analyses)</SelectItem>
                  <SelectItem value="viewer">Viewer (Read-only access)</SelectItem>
                  <SelectItem value="admin">Admin (Manage members & billing)</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setIsInviteOpen(false)}>Cancel</Button>
            <Button 
              disabled={inviteMutation.isPending || !inviteEmail.trim()}
              onClick={() => inviteMutation.mutate({ email: inviteEmail.trim(), role: inviteRole })}
              className="bg-indigo-600 hover:bg-indigo-700 text-white"
            >
              {inviteMutation.isPending ? "Sending Invite..." : "Send Invitation"}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}

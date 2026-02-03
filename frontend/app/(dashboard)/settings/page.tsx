"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { userApi, authApi } from "@/lib/api";
import { useAuthStore, useThemeStore } from "@/lib/store";
import {
  Loader2,
  ArrowLeft,
  Moon,
  Sun,
  MessageCircle,
  User,
  Bell,
  Check,
} from "lucide-react";
import { cn } from "@/lib/utils";

export default function SettingsPage() {
  const router = useRouter();
  const queryClient = useQueryClient();
  const { user, isAuthenticated, setUser, logout } = useAuthStore();
  const { theme, toggleTheme } = useThemeStore();

  const [name, setName] = useState(user?.name || "");
  const [phone, setPhone] = useState(user?.phone_whatsapp || "");
  const [timezone, setTimezone] = useState(user?.timezone || "UTC");
  const [success, setSuccess] = useState("");

  useEffect(() => {
    if (!isAuthenticated) {
      router.push("/login");
    }
  }, [isAuthenticated, router]);

  useEffect(() => {
    if (user) {
      setName(user.name || "");
      setPhone(user.phone_whatsapp || "");
      setTimezone(user.timezone || "UTC");
    }
  }, [user]);

  // Update profile mutation
  const updateProfileMutation = useMutation({
    mutationFn: async (data: any) => {
      const response = await userApi.updateProfile(data);
      return response.data;
    },
    onSuccess: (data) => {
      setUser(data);
      setSuccess("Profile updated successfully");
      setTimeout(() => setSuccess(""), 3000);
    },
  });

  // Connect WhatsApp mutation
  const connectWhatsAppMutation = useMutation({
    mutationFn: async (phoneNumber: string) => {
      const response = await userApi.connectWhatsApp(phoneNumber);
      return response.data;
    },
    onSuccess: async () => {
      const response = await authApi.me();
      setUser(response.data);
      setSuccess("WhatsApp connected! Follow the instructions to complete setup.");
      setTimeout(() => setSuccess(""), 5000);
    },
  });

  const handleSaveProfile = () => {
    updateProfileMutation.mutate({ name, timezone });
  };

  const handleConnectWhatsApp = () => {
    if (phone) {
      connectWhatsAppMutation.mutate(phone);
    }
  };

  const handleLogout = () => {
    logout();
    router.push("/");
  };

  if (!isAuthenticated) return null;

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b sticky top-0 bg-background z-50">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <Link href="/dashboard">
              <Button variant="ghost" size="icon">
                <ArrowLeft className="h-5 w-5" />
              </Button>
            </Link>
            <h1 className="text-xl font-semibold">Settings</h1>
          </div>
          <Button variant="ghost" size="icon" onClick={toggleTheme}>
            {theme === "light" ? (
              <Moon className="h-5 w-5" />
            ) : (
              <Sun className="h-5 w-5" />
            )}
          </Button>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8 max-w-2xl space-y-6">
        {success && (
          <div className="p-4 bg-green-50 dark:bg-green-950 text-green-700 dark:text-green-300 rounded-lg flex items-center space-x-2">
            <Check className="h-5 w-5" />
            <span>{success}</span>
          </div>
        )}

        {/* Profile Settings */}
        <Card>
          <CardHeader>
            <div className="flex items-center space-x-2">
              <User className="h-5 w-5 text-primary" />
              <CardTitle>Profile</CardTitle>
            </div>
            <CardDescription>
              Manage your personal information
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <label className="text-sm font-medium">Email</label>
              <Input value={user?.email || ""} disabled />
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium">Name</label>
              <Input
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Your name"
              />
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium">Timezone</label>
              <select
                value={timezone}
                onChange={(e) => setTimezone(e.target.value)}
                className="w-full h-10 px-3 rounded-md border border-input bg-background text-sm"
              >
                <option value="UTC">UTC</option>
                <option value="America/New_York">Eastern Time (ET)</option>
                <option value="America/Chicago">Central Time (CT)</option>
                <option value="America/Denver">Mountain Time (MT)</option>
                <option value="America/Los_Angeles">Pacific Time (PT)</option>
                <option value="Europe/London">London (GMT)</option>
                <option value="Europe/Paris">Paris (CET)</option>
                <option value="Asia/Kolkata">India (IST)</option>
                <option value="Asia/Tokyo">Tokyo (JST)</option>
                <option value="Asia/Shanghai">China (CST)</option>
                <option value="Australia/Sydney">Sydney (AEST)</option>
              </select>
            </div>
            <Button
              onClick={handleSaveProfile}
              disabled={updateProfileMutation.isPending}
            >
              {updateProfileMutation.isPending ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Saving...
                </>
              ) : (
                "Save Changes"
              )}
            </Button>
          </CardContent>
        </Card>

        {/* WhatsApp Settings */}
        <Card
          className={cn(
            user?.whatsapp_connected === "connected" &&
              "border-green-500 dark:border-green-700"
          )}
        >
          <CardHeader>
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <MessageCircle className="h-5 w-5 text-green-600" />
                <CardTitle>WhatsApp</CardTitle>
              </div>
              {user?.whatsapp_connected === "connected" && (
                <span className="text-xs bg-green-100 text-green-700 dark:bg-green-900 dark:text-green-300 px-2 py-1 rounded-full">
                  Connected
                </span>
              )}
            </div>
            <CardDescription>
              Get daily learning hooks delivered to your WhatsApp
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <label className="text-sm font-medium">WhatsApp Number</label>
              <Input
                value={phone}
                onChange={(e) => setPhone(e.target.value)}
                placeholder="+1234567890"
              />
              <p className="text-xs text-muted-foreground">
                Include country code (e.g., +1 for US, +91 for India)
              </p>
            </div>
            <Button
              onClick={handleConnectWhatsApp}
              disabled={!phone || connectWhatsAppMutation.isPending}
              variant={
                user?.whatsapp_connected === "connected" ? "outline" : "default"
              }
            >
              {connectWhatsAppMutation.isPending ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Connecting...
                </>
              ) : user?.whatsapp_connected === "connected" ? (
                "Update Number"
              ) : (
                "Connect WhatsApp"
              )}
            </Button>

            {user?.whatsapp_connected !== "connected" && (
              <div className="p-4 bg-muted rounded-lg">
                <h4 className="font-medium mb-2">Setup Instructions:</h4>
                <ol className="text-sm text-muted-foreground space-y-2 list-decimal list-inside">
                  <li>Enter your WhatsApp number above and click Connect</li>
                  <li>
                    Save the Twilio number{" "}
                    <strong>+1 415 523 8886</strong> in your contacts
                  </li>
                  <li>
                    Send the message{" "}
                    <code className="bg-background px-1 rounded">
                      join &lt;sandbox-code&gt;
                    </code>{" "}
                    to that number
                  </li>
                  <li>You&apos;ll start receiving daily hooks!</li>
                </ol>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Appearance Settings */}
        <Card>
          <CardHeader>
            <div className="flex items-center space-x-2">
              {theme === "light" ? (
                <Sun className="h-5 w-5 text-primary" />
              ) : (
                <Moon className="h-5 w-5 text-primary" />
              )}
              <CardTitle>Appearance</CardTitle>
            </div>
            <CardDescription>Customize how DailyDev looks</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex items-center justify-between">
              <div>
                <p className="font-medium">Theme</p>
                <p className="text-sm text-muted-foreground">
                  {theme === "light" ? "Light mode" : "Dark mode"}
                </p>
              </div>
              <Button variant="outline" onClick={toggleTheme}>
                {theme === "light" ? (
                  <>
                    <Moon className="mr-2 h-4 w-4" />
                    Dark
                  </>
                ) : (
                  <>
                    <Sun className="mr-2 h-4 w-4" />
                    Light
                  </>
                )}
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Danger Zone */}
        <Card className="border-destructive/50">
          <CardHeader>
            <CardTitle className="text-destructive">Danger Zone</CardTitle>
            <CardDescription>Irreversible actions</CardDescription>
          </CardHeader>
          <CardContent>
            <Button variant="destructive" onClick={handleLogout}>
              Log Out
            </Button>
          </CardContent>
        </Card>
      </main>
    </div>
  );
}

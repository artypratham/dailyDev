import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { Providers } from "./providers";

const inter = Inter({ subsets: ["latin"], variable: "--font-geist-sans" });

export const metadata: Metadata = {
  title: "DailyDev - Free Daily Interview Prep",
  description:
    "Transform interview preparation into a daily habit through bite-sized, real-world problem-driven learning delivered via WhatsApp.",
  keywords: [
    "interview prep",
    "software engineering",
    "DSA",
    "system design",
    "coding interviews",
    "daily learning",
  ],
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className}>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}

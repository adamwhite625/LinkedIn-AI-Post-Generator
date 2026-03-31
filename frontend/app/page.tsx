"use client";

import Link from "next/link";
import {
  SignedIn,
  SignedOut,
  SignInButton,
  UserButton,
} from "@clerk/nextjs";

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-12">

        {/* Navigation */}
        <nav className="flex justify-between items-center mb-16">
          <h1 className="text-2xl font-bold text-gray-800">
            LinkedInGen Pro
          </h1>

          <div className="flex items-center gap-4">
            <SignedOut>
              <SignInButton mode="modal">
                <button className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-6 rounded-lg">
                  Sign In
                </button>
              </SignInButton>
            </SignedOut>

            <SignedIn>
              <Link
                href="/product"
                className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-6 rounded-lg"
              >
                Go to App
              </Link>
              <UserButton showName />
            </SignedIn>
          </div>
        </nav>

        {/* Hero */}
        <section className="text-center py-24">
          <h2 className="text-6xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent mb-6">
            Create Engaging
            <br />
            LinkedIn Posts with AI
          </h2>

          <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
            Build your personal brand with AI-crafted LinkedIn content —
            faster, smarter, better.
          </p>

          {/* Pricing preview */}
          <div className="bg-white/80 backdrop-blur rounded-xl p-6 max-w-sm mx-auto mb-10">
            <h3 className="text-2xl font-bold mb-2">
              Premium Plan
            </h3>
            <p className="text-4xl font-bold text-blue-600 mb-2">
              $10<span className="text-lg text-gray-600">/month</span>
            </p>
            <ul className="text-left text-gray-600">
              <li>✓ Unlimited post generation</li>
              <li>✓ Advanced AI prompts</li>
              <li>✓ Priority access</li>
            </ul>
          </div>

          <SignedOut>
            <SignInButton mode="modal">
              <button className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-bold py-4 px-10 rounded-xl text-lg hover:scale-105 transition">
                Start Free
              </button>
            </SignInButton>
          </SignedOut>

          <SignedIn>
            <Link href="/product">
              <button className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-bold py-4 px-10 rounded-xl text-lg hover:scale-105 transition">
                Access Generator
              </button>
            </Link>
          </SignedIn>
        </section>
      </div>
    </main>
  );
}
"use client";

import { useEffect, useState } from "react";
import { useAuth } from "@clerk/nextjs";
import { Protect, PricingTable, UserButton } from "@clerk/nextjs";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import remarkBreaks from "remark-breaks";

/* -----------------------------
   Generator Component
------------------------------ */
function PostGenerator() {
  const { getToken } = useAuth();
  const [post, setPost] = useState("…loading");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let buffer = "";

    const fetchPost = async () => {
      const token = await getToken();

      if (!token) {
        setPost("Authentication required");
        setLoading(false);
        return;
      }

      const response = await fetch(
        "http://localhost:8000/api/generate",
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (!response.body) {
        setPost("Failed to generate post");
        setLoading(false);
        return;
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      while (true) {
        const { done, value } = await reader.read();
        if (done) {
          setLoading(false);
          break;
        }

        const chunk = decoder.decode(value);
        const lines = chunk.split("\n");

        for (const line of lines) {
          if (line.startsWith("data: ")) {
            buffer += line.replace("data: ", "");
            setPost(buffer);
          }
        }
      }
    };

    fetchPost();
  }, [getToken]);

  return (
    <div className="container mx-auto px-4 py-12">
      {/* Header */}
      <header className="text-center mb-12">
        <h1 className="text-5xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent mb-4">
          LinkedIn Post Generator
        </h1>
        <p className="text-gray-600 text-lg">
          AI-powered professional content at your fingertips
        </p>
      </header>

      {/* Content */}
      <div className="max-w-3xl mx-auto">
        <div className="bg-white rounded-2xl shadow-xl p-8">
          {loading ? (
            <div className="flex items-center justify-center py-12">
              <div className="animate-pulse text-gray-400">
                Generating your LinkedIn post...
              </div>
            </div>
          ) : (
            <div className="prose max-w-none text-gray-700">
              <ReactMarkdown
                remarkPlugins={[remarkGfm, remarkBreaks]}
              >
                {post}
              </ReactMarkdown>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

/* -----------------------------
   Page Wrapper + Subscription
------------------------------ */
export default function ProductPage() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* User menu */}
      <div className="absolute top-4 right-4">
        <UserButton showName />
      </div>

      <Protect
        plan="free_user"
        fallback={
          <div className="container mx-auto px-4 py-20">
            <header className="text-center mb-12">
              <h1 className="text-5xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent mb-4">
                Upgrade to Premium
              </h1>
              <p className="text-gray-600 text-lg">
                Unlock unlimited AI-powered LinkedIn posts
              </p>
            </header>

            <div className="max-w-4xl mx-auto">
              <PricingTable />
            </div>
          </div>
        }
      >
        <PostGenerator />
      </Protect>
    </main>
  );
}
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { ReactQueryDevtools } from "@tanstack/react-query-devtools";

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { useState } from "react";

// Create a client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 1000,
      retry: 1,
    },
  },
});

function App() {
  const [message] = useState("Welcome to FastAPI + React!");
  return (
    <QueryClientProvider client={queryClient}>
      <div className="min-h-screen bg-background p-8">
        <div className="container mx-auto">
          <Card className="w-full max-w-2xl mx-auto">
            <CardHeader>
              <CardTitle className="text-4xl font-bold tracking-tight">
                {message}
              </CardTitle>
              <CardDescription className="text-lg">
                Start building your full-stack application with FastAPI and
                React
              </CardDescription>
            </CardHeader>
            <CardContent></CardContent>
          </Card>
        </div>
      </div>
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  );
}

export default App;

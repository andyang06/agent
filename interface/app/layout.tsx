import './globals.css'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'CrewAI Agent Chat',
  description: 'Chat with your deployed CrewAI agent',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}


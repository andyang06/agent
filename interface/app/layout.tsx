import './globals.css'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'E.D.I.T.H - Enhanced Digital Intelligence & Tactical Helper',
  description: 'Your personal AI assistant, powered by advanced agent technology',
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

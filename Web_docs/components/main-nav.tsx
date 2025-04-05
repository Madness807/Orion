"use client"

import { useState } from "react"
import Link from "next/link"
import { usePathname } from "next/navigation"
import { cn } from "@/lib/utils"
import {
  Home,
  Settings,
  Server,
  Network,
  Smile,
  Brain,
  Camera,
  MessageSquare,
  FileCode,
  HardDrive,
  TestTube,
  HelpCircle,
  Menu,
  X,
} from "lucide-react"

const navItems = [
  { href: "/", label: "Introduction", icon: Home },
  { href: "/installation", label: "Installation", icon: Settings },
  { href: "/architecture", label: "Architecture", icon: Server },
  { href: "/protocole", label: "Protocole MCP", icon: Network },
  { href: "/emotions", label: "Émotions", icon: Smile },
  { href: "/modules", label: "Modules", icon: Brain },
  { href: "/capteurs", label: "Capteurs", icon: Camera },
  { href: "/expressions", label: "Expressions", icon: MessageSquare },
  { href: "/schemas", label: "Schémas", icon: FileCode },
  { href: "/interface-hardware", label: "Matériel", icon: HardDrive },
  { href: "/tests", label: "Tests", icon: TestTube },
  { href: "/depannage", label: "Dépannage", icon: HelpCircle },
]

export function MainNav() {
  const pathname = usePathname()
  const [isOpen, setIsOpen] = useState(false)

  return (
    <>
      <button
        className="fixed left-4 top-4 z-50 rounded-md bg-primary p-2 text-primary-foreground shadow-md md:hidden"
        onClick={() => setIsOpen(!isOpen)}
      >
        {isOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
      </button>

      <nav
        className={cn(
          "fixed inset-y-0 left-0 z-40 w-64 transform bg-card p-4 shadow-lg transition-transform duration-200 ease-in-out md:translate-x-0",
          isOpen ? "translate-x-0" : "-translate-x-full",
        )}
      >
        <div className="mt-16 md:mt-0">
          <ul className="space-y-2">
            {navItems.map((item) => {
              const Icon = item.icon
              const isActive = pathname === item.href

              return (
                <li key={item.href}>
                  <Link
                    href={item.href}
                    className={cn(
                      "flex items-center rounded-md px-3 py-2 text-sm font-medium transition-colors hover:bg-accent hover:text-accent-foreground",
                      isActive ? "bg-accent text-accent-foreground" : "text-muted-foreground",
                    )}
                    onClick={() => setIsOpen(false)}
                  >
                    <Icon className="mr-2 h-5 w-5" />
                    {item.label}
                  </Link>
                </li>
              )
            })}
          </ul>
        </div>
      </nav>

      {/* Overlay to close menu on mobile */}
      {isOpen && (
        <div
          className="fixed inset-0 z-30 bg-background/80 backdrop-blur-sm md:hidden"
          onClick={() => setIsOpen(false)}
        />
      )}
    </>
  )
}


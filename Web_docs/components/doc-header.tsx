import { BotIcon as RobotIcon } from "lucide-react"

export function DocHeader() {
  return (
    <header className="bg-card py-6 shadow-md">
      <div className="container mx-auto flex flex-col items-center justify-center px-4 text-center">
        <div className="flex items-center gap-2">
          <RobotIcon className="h-10 w-10 text-primary" />
          <h1 className="text-3xl font-bold tracking-tight md:text-4xl">Robot Mignon avec ESP32 & NAS</h1>
        </div>
        <p className="mt-2 text-lg text-muted-foreground">
          Un robot expressif, intelligent et mignon capable d&apos;interagir avec son environnement
        </p>
      </div>
    </header>
  )
}


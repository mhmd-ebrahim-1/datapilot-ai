import { useState, useEffect } from "react"

const TOAST_TIMEOUT = 5000

export interface ToastProps {
  id: string
  title?: string
  description?: string
  action?: React.ReactNode
  variant?: "default" | "destructive"
}

type ToastActionElement = React.ReactElement

export function useToast() {
  const [toasts, setToasts] = useState<ToastProps[]>([])

  useEffect(() => {
    if (toasts.length > 0) {
      const timer = setTimeout(() => {
        setToasts((t) => t.slice(1))
      }, TOAST_TIMEOUT)
      return () => clearTimeout(timer)
    }
  }, [toasts])

  return {
    toast: (props: Omit<ToastProps, "id">) => {
      setToasts((t) => [...t, { ...props, id: Math.random().toString() }])
    },
    toasts,
    dismiss: (id: string) => setToasts((t) => t.filter((toast) => toast.id !== id)),
  }
}

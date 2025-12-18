"""
Stats card component
"""
'use client'

import React, { ReactNode } from 'react'

interface StatsCardProps {
  title: string
  value: number | string
  subtitle: string
  icon: ReactNode
}

export default function StatsCard({ title, value, subtitle, icon }: StatsCardProps) {
  return (
    <div className="bg-slate-800 rounded-lg border border-slate-700 p-6 hover:border-blue-500 transition">
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <p className="text-slate-400 text-sm font-medium">{title}</p>
          <p className="text-3xl font-bold text-white mt-2">{value}</p>
          <p className="text-slate-500 text-sm mt-1">{subtitle}</p>
        </div>
        <div className="text-slate-600">
          {icon}
        </div>
      </div>
    </div>
  )
}

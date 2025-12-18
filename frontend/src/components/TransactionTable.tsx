"""
Transaction table component
"""
'use client'

import React from 'react'
import { Trash2, Check, AlertCircle } from 'lucide-react'

interface Transaction {
  id: number
  description: string
  amount: number
  predictedCategory: string
  predictedConfidence: number
  actualCategory?: string
  isCorrected: boolean
  createdAt: string
}

interface TransactionTableProps {
  transactions: Transaction[]
}

export default function TransactionTable({ transactions }: TransactionTableProps) {
  const getCategoryColor = (category: string) => {
    const colors: Record<string, string> = {
      Food: 'bg-orange-500/20 text-orange-400',
      Transport: 'bg-blue-500/20 text-blue-400',
      Bills: 'bg-red-500/20 text-red-400',
      Shopping: 'bg-pink-500/20 text-pink-400',
      Entertainment: 'bg-purple-500/20 text-purple-400',
      'Work Supplies': 'bg-green-500/20 text-green-400',
      Health: 'bg-yellow-500/20 text-yellow-400',
      Other: 'bg-slate-500/20 text-slate-400',
    }
    return colors[category] || 'bg-slate-500/20 text-slate-400'
  }

  return (
    <div className="bg-slate-800 rounded-lg border border-slate-700 overflow-hidden">
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead className="bg-slate-700 border-b border-slate-600">
            <tr>
              <th className="px-6 py-4 text-left font-medium text-slate-300">Description</th>
              <th className="px-6 py-4 text-left font-medium text-slate-300">Amount</th>
              <th className="px-6 py-4 text-left font-medium text-slate-300">Category</th>
              <th className="px-6 py-4 text-left font-medium text-slate-300">Confidence</th>
              <th className="px-6 py-4 text-left font-medium text-slate-300">Status</th>
              <th className="px-6 py-4 text-left font-medium text-slate-300">Action</th>
            </tr>
          </thead>
          <tbody>
            {transactions.length === 0 ? (
              <tr>
                <td colSpan={6} className="px-6 py-8 text-center text-slate-400">
                  No transactions yet. Import a CSV file or categorize manually.
                </td>
              </tr>
            ) : (
              transactions.map((tx) => (
                <tr key={tx.id} className="border-b border-slate-700 hover:bg-slate-700/50 transition">
                  <td className="px-6 py-4 text-slate-300">{tx.description}</td>
                  <td className="px-6 py-4 text-slate-300 font-medium">${tx.amount.toFixed(2)}</td>
                  <td className="px-6 py-4">
                    <span className={`px-3 py-1 rounded-full text-xs font-medium ${getCategoryColor(tx.predictedCategory)}`}>
                      {tx.predictedCategory}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-slate-300">
                    {(tx.predictedConfidence * 100).toFixed(0)}%
                  </td>
                  <td className="px-6 py-4">
                    {tx.predictedConfidence > 0.7 ? (
                      <div className="flex items-center gap-1 text-green-400">
                        <Check className="w-4 h-4" />
                        <span className="text-xs">High</span>
                      </div>
                    ) : tx.predictedConfidence > 0.5 ? (
                      <div className="flex items-center gap-1 text-yellow-400">
                        <AlertCircle className="w-4 h-4" />
                        <span className="text-xs">Medium</span>
                      </div>
                    ) : (
                      <div className="flex items-center gap-1 text-red-400">
                        <AlertCircle className="w-4 h-4" />
                        <span className="text-xs">Low</span>
                      </div>
                    )}
                  </td>
                  <td className="px-6 py-4">
                    <button className="text-slate-400 hover:text-red-400 transition">
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  )
}

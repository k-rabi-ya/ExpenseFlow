"""
Categorization form component
"""
'use client'

import React, { useState } from 'react'
import { Send, Loader } from 'lucide-react'
import api from '../utils/api'
import { useTransactionStore } from '../utils/store'

export default function CategorizationForm() {
  const [description, setDescription] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const { addTransaction } = useTransactionStore()

  const handleCategorize = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!description.trim()) return

    setLoading(true)
    try {
      const response = await api.categorize(description)
      setResult(response)

      // Add to store
      addTransaction({
        id: Date.now(),
        description: response.description,
        amount: 0,
        predictedCategory: response.category,
        predictedConfidence: response.confidence,
        isCorrected: false,
        createdAt: new Date().toISOString(),
      })

      setDescription('')
    } catch (error) {
      console.error('Categorization error:', error)
      setResult({ error: 'Failed to categorize transaction' })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="bg-slate-800 rounded-lg border border-slate-700 p-8">
      <h2 className="text-2xl font-bold text-white mb-6">Categorize Transaction</h2>

      <form onSubmit={handleCategorize} className="mb-6">
        <div className="flex gap-3">
          <input
            type="text"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Enter transaction description (e.g., 'Starbucks coffee')"
            className="flex-1 bg-slate-700 border border-slate-600 rounded-lg px-4 py-3 text-white placeholder-slate-400 focus:outline-none focus:border-blue-500 transition"
          />
          <button
            type="submit"
            disabled={loading}
            className="bg-blue-600 hover:bg-blue-700 disabled:bg-slate-600 text-white px-6 py-3 rounded-lg font-medium transition flex items-center gap-2"
          >
            {loading ? (
              <>
                <Loader className="w-4 h-4 animate-spin" />
                Analyzing...
              </>
            ) : (
              <>
                <Send className="w-4 h-4" />
                Categorize
              </>
            )}
          </button>
        </div>
      </form>

      {result && !result.error && (
        <div className="bg-slate-700 rounded-lg p-6 border border-green-500/30">
          <p className="text-slate-300 mb-4">
            <span className="font-medium text-white">Transaction:</span> {result.description}
          </p>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <p className="text-slate-400 text-sm">Category</p>
              <p className="text-2xl font-bold text-white">{result.category}</p>
            </div>
            <div>
              <p className="text-slate-400 text-sm">Confidence</p>
              <p className="text-2xl font-bold text-green-400">{(result.confidence * 100).toFixed(0)}%</p>
            </div>
          </div>
        </div>
      )}

      {result?.error && (
        <div className="bg-red-500/20 border border-red-500/50 rounded-lg p-4 text-red-400">
          {result.error}
        </div>
      )}
    </div>
  )
}

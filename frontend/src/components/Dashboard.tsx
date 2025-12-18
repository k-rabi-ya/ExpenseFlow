"""
Dashboard component - main entry point
"""
'use client'

import React, { useState } from 'react'
import { Upload, Plus, FileText } from 'lucide-react'
import TransactionTable from './TransactionTable'
import CategorizationForm from './CategorizationForm'
import StatsCard from './StatsCard'
import { useTransactionStore } from '../utils/store'

export default function Dashboard() {
  const [activeTab, setActiveTab] = useState('dashboard')
  const { transactions } = useTransactionStore()
  const categorizedCount = transactions.filter(t => t.predictedConfidence > 0.5).length
  const uncategorizedCount = transactions.length - categorizedCount
  const totalAmount = transactions.reduce((sum, t) => sum + t.amount, 0)

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      {/* Header */}
      <header className="bg-slate-800 border-b border-slate-700 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <h1 className="text-3xl font-bold text-white">ExpenseFlow</h1>
          <p className="text-slate-400 text-sm">Zero-effort expense categorization</p>
        </div>
      </header>

      {/* Navigation Tabs */}
      <div className="max-w-7xl mx-auto px-6 mt-8">
        <div className="flex gap-4 mb-6">
          <button
            onClick={() => setActiveTab('dashboard')}
            className={`px-4 py-2 rounded-lg font-medium transition ${
              activeTab === 'dashboard'
                ? 'bg-blue-600 text-white'
                : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
            }`}
          >
            Dashboard
          </button>
          <button
            onClick={() => setActiveTab('categorize')}
            className={`px-4 py-2 rounded-lg font-medium transition ${
              activeTab === 'categorize'
                ? 'bg-blue-600 text-white'
                : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
            }`}
          >
            Categorize
          </button>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-6 pb-12">
        {activeTab === 'dashboard' && (
          <div>
            {/* Stats Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
              <StatsCard
                title="Total Transactions"
                value={transactions.length}
                subtitle={`$${totalAmount.toFixed(2)}`}
                icon={<FileText className="w-6 h-6" />}
              />
              <StatsCard
                title="Categorized"
                value={categorizedCount}
                subtitle={`${((categorizedCount / transactions.length) * 100 || 0).toFixed(0)}%`}
                icon={<Plus className="w-6 h-6" />}
              />
              <StatsCard
                title="Uncategorized"
                value={uncategorizedCount}
                subtitle="Needs review"
                icon={<Upload className="w-6 h-6" />}
              />
            </div>

            {/* Import Area */}
            <div className="bg-slate-800 rounded-lg border border-slate-700 p-8 mb-8 text-center hover:border-blue-500 transition">
              <Upload className="w-12 h-12 mx-auto mb-4 text-slate-400" />
              <p className="text-white font-medium mb-2">Import Transactions</p>
              <p className="text-slate-400 text-sm mb-4">Drag and drop CSV file or click to browse</p>
              <input
                type="file"
                accept=".csv"
                className="hidden"
                id="csv-input"
              />
              <label
                htmlFor="csv-input"
                className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg font-medium cursor-pointer transition"
              >
                Browse Files
              </label>
            </div>

            {/* Transaction Table */}
            <TransactionTable transactions={transactions} />
          </div>
        )}

        {activeTab === 'categorize' && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <div className="lg:col-span-2">
              <CategorizationForm />
            </div>
            <div className="bg-slate-800 rounded-lg border border-slate-700 p-6">
              <h3 className="text-white font-medium mb-4">Categories</h3>
              <div className="space-y-2 text-slate-300 text-sm">
                <p>🍔 Food</p>
                <p>🚗 Transport</p>
                <p>💳 Bills</p>
                <p>🛍️ Shopping</p>
                <p>🎬 Entertainment</p>
                <p>💼 Work Supplies</p>
                <p>🏥 Health</p>
                <p>📦 Other</p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

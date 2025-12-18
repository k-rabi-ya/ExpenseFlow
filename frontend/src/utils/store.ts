"""
Store for transaction state management
"""
import create from "zustand"

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

interface TransactionStore {
  transactions: Transaction[]
  addTransaction: (transaction: Transaction) => void
  updateTransaction: (id: number, updates: Partial<Transaction>) => void
  removeTransaction: (id: number) => void
  clearTransactions: () => void
  getCategorizedCount: () => number
  getUncategorizedCount: () => number
}

export const useTransactionStore = create<TransactionStore>((set, get) => ({
  transactions: [],

  addTransaction: (transaction) =>
    set((state) => ({
      transactions: [...state.transactions, transaction],
    })),

  updateTransaction: (id, updates) =>
    set((state) => ({
      transactions: state.transactions.map((t) =>
        t.id === id ? { ...t, ...updates } : t
      ),
    })),

  removeTransaction: (id) =>
    set((state) => ({
      transactions: state.transactions.filter((t) => t.id !== id),
    })),

  clearTransactions: () => set({ transactions: [] }),

  getCategorizedCount: () =>
    get().transactions.filter((t) => t.predictedConfidence > 0.5).length,

  getUncategorizedCount: () =>
    get().transactions.filter((t) => t.predictedConfidence <= 0.5).length,
}))

export default useTransactionStore

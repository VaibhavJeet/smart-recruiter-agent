'use client'

import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { Upload, Search, User } from 'lucide-react'
import { api } from '@/lib/api'
import { ResumeUploader } from '@/components/ResumeUploader'

export default function CandidatesPage() {
  const [showUploader, setShowUploader] = useState(false)
  const queryClient = useQueryClient()

  const { data: candidates, isLoading } = useQuery({
    queryKey: ['candidates'],
    queryFn: () => api.getCandidates(),
  })

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <a href="/" className="text-xl font-bold text-primary-600">Smart Recruiter</a>
              <span className="ml-4 text-gray-500">/</span>
              <span className="ml-4 text-gray-900">Candidates</span>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-semibold text-gray-900">Candidates</h2>
            <button
              onClick={() => setShowUploader(true)}
              className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700"
            >
              <Upload className="h-4 w-4 mr-2" />
              Upload Resume
            </button>
          </div>

          {showUploader && (
            <div className="mb-6">
              <ResumeUploader
                onSuccess={() => {
                  setShowUploader(false)
                  queryClient.invalidateQueries({ queryKey: ['candidates'] })
                }}
                onCancel={() => setShowUploader(false)}
              />
            </div>
          )}

          <div className="bg-white shadow rounded-lg">
            {isLoading ? (
              <div className="p-6 text-center text-gray-500">Loading...</div>
            ) : candidates?.length === 0 ? (
              <div className="p-6 text-center text-gray-500">
                No candidates yet. Upload a resume to get started.
              </div>
            ) : (
              <ul className="divide-y divide-gray-200">
                {candidates?.map((candidate: any) => (
                  <li key={candidate.id} className="p-6 hover:bg-gray-50">
                    <div className="flex items-center">
                      <div className="flex-shrink-0">
                        <div className="h-10 w-10 rounded-full bg-primary-100 flex items-center justify-center">
                          <User className="h-5 w-5 text-primary-600" />
                        </div>
                      </div>
                      <div className="ml-4 flex-1">
                        <div className="flex items-center justify-between">
                          <p className="text-sm font-medium text-gray-900">{candidate.name}</p>
                          <span className={`px-2 py-1 text-xs rounded-full ${
                            candidate.status === 'new' ? 'bg-blue-100 text-blue-800' :
                            candidate.status === 'screening' ? 'bg-yellow-100 text-yellow-800' :
                            candidate.status === 'interview' ? 'bg-purple-100 text-purple-800' :
                            'bg-gray-100 text-gray-800'
                          }`}>
                            {candidate.status}
                          </span>
                        </div>
                        <p className="text-sm text-gray-500">{candidate.email}</p>
                        <div className="mt-2 flex flex-wrap gap-1">
                          {candidate.skills?.slice(0, 5).map((skill: string) => (
                            <span key={skill} className="px-2 py-0.5 text-xs bg-gray-100 text-gray-600 rounded">
                              {skill}
                            </span>
                          ))}
                        </div>
                      </div>
                    </div>
                  </li>
                ))}
              </ul>
            )}
          </div>
        </div>
      </main>
    </div>
  )
}
'use client'

import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { Plus, Briefcase, Users } from 'lucide-react'
import { api } from '@/lib/api'

export default function JobsPage() {
  const [showForm, setShowForm] = useState(false)
  const queryClient = useQueryClient()

  const { data: jobs, isLoading } = useQuery({
    queryKey: ['jobs'],
    queryFn: () => api.getJobs(),
  })

  const createJob = useMutation({
    mutationFn: api.createJob,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['jobs'] })
      setShowForm(false)
    },
  })

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    const formData = new FormData(e.currentTarget)
    createJob.mutate({
      title: formData.get('title') as string,
      description: formData.get('description') as string,
      department: formData.get('department') as string,
      location: formData.get('location') as string,
      required_skills: (formData.get('skills') as string).split(',').map(s => s.trim()),
      experience_min: parseInt(formData.get('experience_min') as string) || 0,
    })
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <a href="/" className="text-xl font-bold text-primary-600">Smart Recruiter</a>
              <span className="ml-4 text-gray-500">/</span>
              <span className="ml-4 text-gray-900">Jobs</span>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-semibold text-gray-900">Job Postings</h2>
            <button
              onClick={() => setShowForm(true)}
              className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700"
            >
              <Plus className="h-4 w-4 mr-2" />
              New Job
            </button>
          </div>

          {showForm && (
            <div className="mb-6 bg-white shadow rounded-lg p-6">
              <h3 className="text-lg font-medium mb-4">Create New Job</h3>
              <form onSubmit={handleSubmit} className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Title</label>
                    <input name="title" required className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500" />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Department</label>
                    <input name="department" className="mt-1 block w-full rounded-md border-gray-300 shadow-sm" />
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Description</label>
                  <textarea name="description" required rows={3} className="mt-1 block w-full rounded-md border-gray-300 shadow-sm" />
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Location</label>
                    <input name="location" className="mt-1 block w-full rounded-md border-gray-300 shadow-sm" />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Min Experience (years)</label>
                    <input name="experience_min" type="number" className="mt-1 block w-full rounded-md border-gray-300 shadow-sm" />
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Required Skills (comma-separated)</label>
                  <input name="skills" className="mt-1 block w-full rounded-md border-gray-300 shadow-sm" />
                </div>
                <div className="flex justify-end gap-2">
                  <button type="button" onClick={() => setShowForm(false)} className="px-4 py-2 text-sm text-gray-700 hover:text-gray-900">Cancel</button>
                  <button type="submit" className="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700">Create</button>
                </div>
              </form>
            </div>
          )}

          <div className="bg-white shadow rounded-lg">
            {isLoading ? (
              <div className="p-6 text-center text-gray-500">Loading...</div>
            ) : jobs?.length === 0 ? (
              <div className="p-6 text-center text-gray-500">No jobs posted yet.</div>
            ) : (
              <ul className="divide-y divide-gray-200">
                {jobs?.map((job: any) => (
                  <li key={job.id} className="p-6 hover:bg-gray-50">
                    <div className="flex items-center">
                      <div className="flex-shrink-0">
                        <div className="h-10 w-10 rounded-full bg-green-100 flex items-center justify-center">
                          <Briefcase className="h-5 w-5 text-green-600" />
                        </div>
                      </div>
                      <div className="ml-4 flex-1">
                        <div className="flex items-center justify-between">
                          <p className="text-sm font-medium text-gray-900">{job.title}</p>
                          <span className={`px-2 py-1 text-xs rounded-full ${
                            job.status === 'open' ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
                          }`}>
                            {job.status}
                          </span>
                        </div>
                        <p className="text-sm text-gray-500">{job.department} • {job.location}</p>
                        <p className="text-sm text-gray-400 mt-1">{job.experience_min}+ years experience</p>
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
import axios from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

const client = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const api = {
  // Candidates
  getCandidates: async () => {
    const { data } = await client.get('/api/candidates')
    return data
  },

  getCandidate: async (id: number) => {
    const { data } = await client.get(`/api/candidates/${id}`)
    return data
  },

  uploadResume: async (file: File, name?: string, email?: string) => {
    const formData = new FormData()
    formData.append('file', file)
    if (name) formData.append('name', name)
    if (email) formData.append('email', email)
    const { data } = await client.post('/api/candidates/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    return data
  },

  matchCandidate: async (candidateId: number, jobId: number) => {
    const { data } = await client.post(`/api/candidates/${candidateId}/match/${jobId}`)
    return data
  },

  // Jobs
  getJobs: async () => {
    const { data } = await client.get('/api/jobs')
    return data
  },

  getJob: async (id: number) => {
    const { data } = await client.get(`/api/jobs/${id}`)
    return data
  },

  createJob: async (job: any) => {
    const { data } = await client.post('/api/jobs', job)
    return data
  },

  getJobCandidates: async (jobId: number) => {
    const { data } = await client.get(`/api/jobs/${jobId}/candidates`)
    return data
  },

  // Interviews
  getInterviews: async () => {
    const { data } = await client.get('/api/interviews')
    return data
  },

  scheduleInterview: async (candidateId: number, jobId: number, interviewers: string[]) => {
    const { data } = await client.post('/api/interviews/schedule', null, {
      params: { candidate_id: candidateId, job_id: jobId, interviewers },
    })
    return data
  },

  updateInterview: async (id: number, update: any) => {
    const { data } = await client.patch(`/api/interviews/${id}`, update)
    return data
  },
}
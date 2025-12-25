'use client'

import { useCallback, useState } from 'react'
import { useDropzone } from 'react-dropzone'
import { useMutation } from '@tanstack/react-query'
import { Upload, FileText, Loader2, X } from 'lucide-react'
import { api } from '@/lib/api'

interface ResumeUploaderProps {
  onSuccess: () => void
  onCancel: () => void
}

export function ResumeUploader({ onSuccess, onCancel }: ResumeUploaderProps) {
  const [file, setFile] = useState<File | null>(null)

  const uploadMutation = useMutation({
    mutationFn: (file: File) => api.uploadResume(file),
    onSuccess,
  })

  const onDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0) {
      setFile(acceptedFiles[0])
    }
  }, [])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'text/plain': ['.txt'],
    },
    maxFiles: 1,
  })

  const handleUpload = () => {
    if (file) {
      uploadMutation.mutate(file)
    }
  }

  return (
    <div className="bg-white shadow rounded-lg p-6">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-lg font-medium">Upload Resume</h3>
        <button onClick={onCancel} className="text-gray-400 hover:text-gray-500">
          <X className="h-5 w-5" />
        </button>
      </div>

      {!file ? (
        <div
          {...getRootProps()}
          className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors ${
            isDragActive ? 'border-primary-500 bg-primary-50' : 'border-gray-300 hover:border-gray-400'
          }`}
        >
          <input {...getInputProps()} />
          <Upload className="mx-auto h-12 w-12 text-gray-400" />
          <p className="mt-2 text-sm text-gray-600">
            {isDragActive ? 'Drop the file here...' : 'Drag & drop a resume, or click to select'}
          </p>
          <p className="mt-1 text-xs text-gray-500">PDF, DOCX, or TXT</p>
        </div>
      ) : (
        <div className="border rounded-lg p-4">
          <div className="flex items-center">
            <FileText className="h-8 w-8 text-primary-600" />
            <div className="ml-3 flex-1">
              <p className="text-sm font-medium text-gray-900">{file.name}</p>
              <p className="text-xs text-gray-500">{(file.size / 1024).toFixed(1)} KB</p>
            </div>
            <button onClick={() => setFile(null)} className="text-gray-400 hover:text-gray-500">
              <X className="h-5 w-5" />
            </button>
          </div>
        </div>
      )}

      {uploadMutation.isError && (
        <p className="mt-2 text-sm text-red-600">Error uploading file. Please try again.</p>
      )}

      <div className="mt-4 flex justify-end gap-2">
        <button onClick={onCancel} className="px-4 py-2 text-sm text-gray-700 hover:text-gray-900">
          Cancel
        </button>
        <button
          onClick={handleUpload}
          disabled={!file || uploadMutation.isPending}
          className="inline-flex items-center px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {uploadMutation.isPending ? (
            <>
              <Loader2 className="animate-spin h-4 w-4 mr-2" />
              Processing...
            </>
          ) : (
            'Upload & Parse'
          )}
        </button>
      </div>
    </div>
  )
}
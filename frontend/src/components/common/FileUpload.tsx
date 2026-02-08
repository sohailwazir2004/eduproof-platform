import React, { useCallback, useState } from 'react';
import { Upload, X, File, CheckCircle, AlertCircle } from 'lucide-react';
import { FileUploadProgress } from '../../types';
import Button from '../ui/Button';

interface FileUploadProps {
  accept?: string;
  multiple?: boolean;
  maxSize?: number; // in MB
  onFilesSelected: (files: File[]) => void;
  onUpload?: (files: File[]) => Promise<void>;
  disabled?: boolean;
  className?: string;
}

const FileUpload: React.FC<FileUploadProps> = ({
  accept = 'image/*,application/pdf',
  multiple = false,
  maxSize = 10,
  onFilesSelected,
  onUpload,
  disabled = false,
  className = '',
}) => {
  const [dragActive, setDragActive] = useState(false);
  const [uploadProgress, setUploadProgress] = useState<FileUploadProgress[]>([]);
  const [errors, setErrors] = useState<string[]>([]);

  const validateFile = (file: File): string | null => {
    if (maxSize && file.size > maxSize * 1024 * 1024) {
      return `${file.name} exceeds ${maxSize}MB limit`;
    }
    return null;
  };

  const handleFiles = (files: FileList | null) => {
    if (!files || files.length === 0) return;

    const fileArray = Array.from(files);
    const newErrors: string[] = [];
    const validFiles: File[] = [];

    fileArray.forEach((file) => {
      const error = validateFile(file);
      if (error) {
        newErrors.push(error);
      } else {
        validFiles.push(file);
      }
    });

    if (newErrors.length > 0) {
      setErrors(newErrors);
      setTimeout(() => setErrors([]), 5000);
    }

    if (validFiles.length > 0) {
      const progress: FileUploadProgress[] = validFiles.map((file) => ({
        file,
        progress: 0,
        status: 'pending',
      }));
      setUploadProgress(progress);
      onFilesSelected(validFiles);

      if (onUpload) {
        handleUpload(validFiles);
      }
    }
  };

  const handleUpload = async (files: File[]) => {
    if (!onUpload) return;

    setUploadProgress((prev) =>
      prev.map((item) => ({ ...item, status: 'uploading' }))
    );

    try {
      await onUpload(files);
      setUploadProgress((prev) =>
        prev.map((item) => ({ ...item, status: 'completed', progress: 100 }))
      );
    } catch (error) {
      setUploadProgress((prev) =>
        prev.map((item) => ({
          ...item,
          status: 'error',
          error: 'Upload failed',
        }))
      );
    }
  };

  const handleDrag = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  }, []);

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      e.stopPropagation();
      setDragActive(false);
      if (disabled) return;
      handleFiles(e.dataTransfer.files);
    },
    [disabled]
  );

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    e.preventDefault();
    if (disabled) return;
    handleFiles(e.target.files);
  };

  const removeFile = (index: number) => {
    setUploadProgress((prev) => prev.filter((_, i) => i !== index));
  };

  const formatFileSize = (bytes: number): string => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
  };

  return (
    <div className={`w-full ${className}`}>
      <div
        className={`relative border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
          dragActive
            ? 'border-primary-500 bg-primary-50'
            : 'border-gray-300 bg-gray-50'
        } ${disabled ? 'opacity-50 cursor-not-allowed' : 'hover:border-primary-400'}`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
      >
        <input
          type="file"
          id="file-upload"
          className="absolute inset-0 w-full h-full opacity-0 cursor-pointer disabled:cursor-not-allowed"
          accept={accept}
          multiple={multiple}
          onChange={handleChange}
          disabled={disabled}
        />
        <div className="flex flex-col items-center justify-center space-y-3">
          <div className="p-3 bg-primary-100 rounded-full">
            <Upload className="w-8 h-8 text-primary-600" />
          </div>
          <div>
            <p className="text-lg font-medium text-gray-700">
              Drag and drop files here
            </p>
            <p className="text-sm text-gray-500 mt-1">or click to browse</p>
          </div>
          <p className="text-xs text-gray-400">
            {multiple ? 'Multiple files allowed' : 'Single file only'} • Max{' '}
            {maxSize}MB per file
          </p>
        </div>
      </div>

      {errors.length > 0 && (
        <div className="mt-4 space-y-2">
          {errors.map((error, index) => (
            <div
              key={index}
              className="flex items-center gap-2 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm"
            >
              <AlertCircle className="w-4 h-4 flex-shrink-0" />
              <span>{error}</span>
            </div>
          ))}
        </div>
      )}

      {uploadProgress.length > 0 && (
        <div className="mt-4 space-y-3">
          {uploadProgress.map((item, index) => (
            <div
              key={index}
              className="flex items-center gap-3 p-3 bg-white border border-gray-200 rounded-lg"
            >
              <div className="flex-shrink-0">
                {item.status === 'completed' ? (
                  <CheckCircle className="w-5 h-5 text-green-500" />
                ) : item.status === 'error' ? (
                  <AlertCircle className="w-5 h-5 text-red-500" />
                ) : (
                  <File className="w-5 h-5 text-gray-400" />
                )}
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center justify-between mb-1">
                  <p className="text-sm font-medium text-gray-700 truncate">
                    {item.file.name}
                  </p>
                  <span className="text-xs text-gray-500 ml-2">
                    {formatFileSize(item.file.size)}
                  </span>
                </div>
                {item.status === 'uploading' && (
                  <div className="w-full bg-gray-200 rounded-full h-1.5">
                    <div
                      className="bg-primary-600 h-1.5 rounded-full transition-all duration-300"
                      style={{ width: `${item.progress}%` }}
                    />
                  </div>
                )}
                {item.status === 'error' && item.error && (
                  <p className="text-xs text-red-600">{item.error}</p>
                )}
              </div>
              {item.status !== 'uploading' && (
                <button
                  onClick={() => removeFile(index)}
                  className="flex-shrink-0 p-1 hover:bg-gray-100 rounded transition-colors"
                >
                  <X className="w-4 h-4 text-gray-400" />
                </button>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default FileUpload;

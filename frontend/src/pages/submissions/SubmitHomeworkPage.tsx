import React, { useState } from 'react';
import { useQuery, useMutation } from '@tanstack/react-query';
import { useNavigate, useParams } from 'react-router-dom';
import { ArrowLeft, Upload, Send, CheckCircle } from 'lucide-react';
import Card from '../../components/ui/Card';
import Button from '../../components/ui/Button';
import FileUpload from '../../components/common/FileUpload';
import { homeworkService, submissionService } from '../../services';
import { format } from 'date-fns';

const SubmitHomeworkPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploadProgress, setUploadProgress] = useState(0);

  const { data: homework, isLoading } = useQuery({
    queryKey: ['homework', id],
    queryFn: () => homeworkService.getHomework(id!),
    enabled: !!id,
  });

  const submitMutation = useMutation({
    mutationFn: async (file: File) => {
      return await submissionService.createSubmission(id!, file);
    },
    onSuccess: (data) => {
      navigate(`/submissions/${data.id}`);
    },
    onError: (error) => {
      console.error('Failed to submit homework:', error);
      alert('Failed to submit homework. Please try again.');
    },
  });

  const handleFilesSelected = (files: File[]) => {
    if (files.length > 0) {
      setSelectedFile(files[0]);
    }
  };

  const handleSubmit = async () => {
    if (!selectedFile) {
      alert('Please select a file to upload');
      return;
    }

    submitMutation.mutate(selectedFile);
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  if (!homework) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500">Homework not found</p>
        <Button onClick={() => navigate('/homework')} className="mt-4">
          Back to Homework
        </Button>
      </div>
    );
  }

  const isOverdue = new Date(homework.due_date) < new Date();

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <Button
          variant="ghost"
          icon={<ArrowLeft className="w-5 h-5" />}
          onClick={() => navigate(`/homework/${id}`)}
        >
          Back
        </Button>
      </div>

      <div>
        <h1 className="text-3xl font-bold text-gray-900">Submit Homework</h1>
        <p className="text-gray-600 mt-1">Upload your completed homework</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <Card variant="elevated">
            <Card.Header divider>
              <h2 className="text-xl font-bold text-gray-900">Homework Details</h2>
            </Card.Header>
            <div className="p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-2">{homework.title}</h3>
              {homework.description && (
                <p className="text-gray-600 mb-4">{homework.description}</p>
              )}
              <div className="flex items-center gap-4 text-sm text-gray-600">
                <div>
                  <span className="font-medium">Due Date:</span>{' '}
                  {format(new Date(homework.due_date), 'MMMM dd, yyyy hh:mm a')}
                </div>
                {homework.page_numbers && (
                  <div>
                    <span className="font-medium">Pages:</span> {homework.page_numbers}
                  </div>
                )}
              </div>
              {isOverdue && (
                <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-lg">
                  <p className="text-sm text-red-700 font-medium">
                    This homework is overdue. Late submissions may be penalized.
                  </p>
                </div>
              )}
            </div>
          </Card>

          <Card variant="elevated">
            <Card.Header divider>
              <h2 className="text-xl font-bold text-gray-900">Upload Your Work</h2>
            </Card.Header>
            <div className="p-6">
              <FileUpload
                accept="image/*,application/pdf"
                multiple={false}
                maxSize={10}
                onFilesSelected={handleFilesSelected}
              />
              {selectedFile && (
                <div className="mt-4 p-4 bg-green-50 border border-green-200 rounded-lg">
                  <div className="flex items-center gap-2 text-green-700">
                    <CheckCircle className="w-5 h-5" />
                    <p className="font-medium">File selected: {selectedFile.name}</p>
                  </div>
                  <p className="text-sm text-green-600 mt-1">
                    Size: {(selectedFile.size / (1024 * 1024)).toFixed(2)} MB
                  </p>
                </div>
              )}
            </div>
          </Card>

          <Card variant="elevated" className="p-6">
            <div className="flex gap-4">
              <Button
                fullWidth
                icon={<Send className="w-5 h-5" />}
                onClick={handleSubmit}
                disabled={!selectedFile || submitMutation.isPending}
                loading={submitMutation.isPending}
              >
                Submit Homework
              </Button>
              <Button
                variant="ghost"
                onClick={() => navigate(`/homework/${id}`)}
                disabled={submitMutation.isPending}
              >
                Cancel
              </Button>
            </div>
          </Card>
        </div>

        <div className="space-y-6">
          <Card variant="elevated">
            <Card.Header divider>
              <h2 className="text-xl font-bold text-gray-900">Submission Guidelines</h2>
            </Card.Header>
            <Card.Body>
              <ul className="space-y-3 text-sm text-gray-600">
                <li className="flex items-start gap-2">
                  <span className="text-primary-600 mt-1">•</span>
                  <span>Upload clear, legible images or PDF files</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-primary-600 mt-1">•</span>
                  <span>Ensure all pages are included in order</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-primary-600 mt-1">•</span>
                  <span>Maximum file size is 10MB</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-primary-600 mt-1">•</span>
                  <span>Supported formats: JPG, PNG, PDF</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-primary-600 mt-1">•</span>
                  <span>Double-check your work before submitting</span>
                </li>
              </ul>
            </Card.Body>
          </Card>

          <Card variant="elevated">
            <Card.Header divider>
              <h2 className="text-xl font-bold text-gray-900">Tips</h2>
            </Card.Header>
            <Card.Body>
              <ul className="space-y-2 text-sm text-gray-600">
                <li className="flex items-start gap-2">
                  <span className="text-primary-600 mt-1">•</span>
                  <span>Write neatly and legibly</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-primary-600 mt-1">•</span>
                  <span>Show your work and calculations</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-primary-600 mt-1">•</span>
                  <span>Use good lighting when taking photos</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-primary-600 mt-1">•</span>
                  <span>Submit before the due date</span>
                </li>
              </ul>
            </Card.Body>
          </Card>

          {isOverdue && (
            <Card variant="elevated" className="border-red-200 bg-red-50">
              <Card.Body>
                <div className="text-center">
                  <p className="text-sm font-medium text-red-700">Overdue Submission</p>
                  <p className="text-xs text-red-600 mt-1">
                    This homework was due on{' '}
                    {format(new Date(homework.due_date), 'MMM dd, yyyy')}
                  </p>
                </div>
              </Card.Body>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
};

export default SubmitHomeworkPage;

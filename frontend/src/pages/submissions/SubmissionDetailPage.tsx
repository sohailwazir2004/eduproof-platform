import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useNavigate, useParams } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import {
  ArrowLeft,
  FileText,
  Calendar,
  User,
  Bot,
  Save,
  CheckCircle,
  Clock,
  Eye,
} from 'lucide-react';
import Card from '../../components/ui/Card';
import Button from '../../components/ui/Button';
import { submissionService, homeworkService, authService } from '../../services';
import { format } from 'date-fns';

const gradeSchema = z.object({
  grade: z.number().min(0, 'Grade must be at least 0').max(100, 'Grade cannot exceed 100'),
  teacher_feedback: z.string().optional(),
});

type GradeFormData = z.infer<typeof gradeSchema>;

const SubmissionDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const userRole = authService.getUserRole();

  const [showGradeForm, setShowGradeForm] = useState(false);

  const { data: submission, isLoading } = useQuery({
    queryKey: ['submission', id],
    queryFn: () => submissionService.getSubmission(id!),
    enabled: !!id,
  });

  const { data: homework } = useQuery({
    queryKey: ['homework', submission?.homework_id],
    queryFn: () => homeworkService.getHomework(submission!.homework_id),
    enabled: !!submission?.homework_id,
  });

  const { data: aiAnalysis } = useQuery({
    queryKey: ['ai-analysis', id],
    queryFn: () => submissionService.getAIAnalysis(id!),
    enabled: !!id && userRole === 'teacher',
  });

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<GradeFormData>({
    resolver: zodResolver(gradeSchema),
    defaultValues: {
      grade: submission?.grade || 0,
      teacher_feedback: submission?.teacher_feedback || '',
    },
  });

  const gradeMutation = useMutation({
    mutationFn: (data: GradeFormData) =>
      submissionService.gradeSubmission(id!, {
        grade: data.grade,
        teacher_feedback: data.teacher_feedback,
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['submission', id] });
      setShowGradeForm(false);
      alert('Grade submitted successfully!');
    },
    onError: (error) => {
      console.error('Failed to submit grade:', error);
      alert('Failed to submit grade. Please try again.');
    },
  });

  const onSubmitGrade = (data: GradeFormData) => {
    gradeMutation.mutate(data);
  };

  const getStatusBadge = (status: string) => {
    const badges = {
      graded: { bg: 'bg-green-100', text: 'text-green-700', icon: CheckCircle },
      reviewed: { bg: 'bg-blue-100', text: 'text-blue-700', icon: Eye },
      pending: { bg: 'bg-yellow-100', text: 'text-yellow-700', icon: Clock },
    };
    const badge = badges[status as keyof typeof badges] || badges.pending;
    const Icon = badge.icon;

    return (
      <span className={`inline-flex items-center gap-1 px-3 py-1 text-sm font-medium rounded-full ${badge.bg} ${badge.text}`}>
        <Icon className="w-4 h-4" />
        {status.charAt(0).toUpperCase() + status.slice(1)}
      </span>
    );
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  if (!submission) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500">Submission not found</p>
        <Button onClick={() => navigate('/submissions')} className="mt-4">
          Back to Submissions
        </Button>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <Button
          variant="ghost"
          icon={<ArrowLeft className="w-5 h-5" />}
          onClick={() => navigate('/submissions')}
        >
          Back
        </Button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <Card variant="elevated">
            <div className="p-6">
              <div className="flex items-start justify-between mb-4">
                <div>
                  <h1 className="text-3xl font-bold text-gray-900 mb-2">Submission Details</h1>
                  {getStatusBadge(submission.status)}
                </div>
                {userRole === 'teacher' && submission.status !== 'graded' && (
                  <Button
                    size="sm"
                    icon={<CheckCircle className="w-4 h-4" />}
                    onClick={() => setShowGradeForm(!showGradeForm)}
                  >
                    Grade Submission
                  </Button>
                )}
              </div>

              <div className="space-y-4">
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <p className="text-gray-600">Submitted At</p>
                    <p className="text-gray-900 font-medium">
                      {format(new Date(submission.submitted_at), 'MMMM dd, yyyy hh:mm a')}
                    </p>
                  </div>
                  {submission.reviewed_at && (
                    <div>
                      <p className="text-gray-600">Reviewed At</p>
                      <p className="text-gray-900 font-medium">
                        {format(new Date(submission.reviewed_at), 'MMMM dd, yyyy hh:mm a')}
                      </p>
                    </div>
                  )}
                  {submission.grade !== undefined && (
                    <div>
                      <p className="text-gray-600">Grade</p>
                      <p className="text-3xl font-bold text-gray-900">{submission.grade}</p>
                    </div>
                  )}
                </div>

                {homework && (
                  <div className="pt-4 border-t border-gray-200">
                    <p className="text-gray-600 text-sm mb-2">Homework Assignment</p>
                    <div className="flex items-center justify-between">
                      <div>
                        <h3 className="font-medium text-gray-900">{homework.title}</h3>
                        <p className="text-sm text-gray-500">
                          Due: {format(new Date(homework.due_date), 'MMM dd, yyyy')}
                        </p>
                      </div>
                      <Button
                        size="sm"
                        variant="ghost"
                        onClick={() => navigate(`/homework/${homework.id}`)}
                      >
                        View Homework
                      </Button>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </Card>

          <Card variant="elevated">
            <Card.Header divider>
              <h2 className="text-xl font-bold text-gray-900">Submitted Work</h2>
            </Card.Header>
            <div className="p-6">
              {submission.file_url ? (
                <div className="space-y-4">
                  {submission.file_type?.startsWith('image/') ? (
                    <img
                      src={submission.file_url}
                      alt="Submission"
                      className="w-full rounded-lg border border-gray-200"
                    />
                  ) : (
                    <div className="flex items-center justify-center p-12 bg-gray-50 rounded-lg border-2 border-dashed border-gray-300">
                      <div className="text-center">
                        <FileText className="w-16 h-16 mx-auto mb-4 text-gray-400" />
                        <p className="text-gray-600 mb-4">
                          {submission.file_type === 'application/pdf'
                            ? 'PDF Document'
                            : 'File'}
                        </p>
                        <a
                          href={submission.file_url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-primary-600 hover:text-primary-700 underline"
                        >
                          Open in New Tab
                        </a>
                      </div>
                    </div>
                  )}
                </div>
              ) : (
                <p className="text-gray-500 text-center py-8">No file attached</p>
              )}
            </div>
          </Card>

          {aiAnalysis && (
            <Card variant="elevated">
              <Card.Header divider>
                <div className="flex items-center gap-2">
                  <Bot className="w-5 h-5 text-purple-600" />
                  <h2 className="text-xl font-bold text-gray-900">AI Analysis</h2>
                </div>
              </Card.Header>
              <div className="p-6">
                <div className="prose max-w-none">
                  <p className="text-gray-700">{aiAnalysis.analysis || 'No AI analysis available'}</p>
                </div>
              </div>
            </Card>
          )}

          {submission.teacher_feedback && !showGradeForm && (
            <Card variant="elevated">
              <Card.Header divider>
                <h2 className="text-xl font-bold text-gray-900">Teacher Feedback</h2>
              </Card.Header>
              <div className="p-6">
                <p className="text-gray-700 leading-relaxed">{submission.teacher_feedback}</p>
              </div>
            </Card>
          )}

          {showGradeForm && userRole === 'teacher' && (
            <Card variant="elevated">
              <Card.Header divider>
                <h2 className="text-xl font-bold text-gray-900">Grade Submission</h2>
              </Card.Header>
              <div className="p-6">
                <form onSubmit={handleSubmit(onSubmitGrade)} className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Grade (0-100) <span className="text-red-500">*</span>
                    </label>
                    <input
                      type="number"
                      {...register('grade', { valueAsNumber: true })}
                      min="0"
                      max="100"
                      className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 ${
                        errors.grade ? 'border-red-500' : 'border-gray-300'
                      }`}
                      placeholder="Enter grade"
                    />
                    {errors.grade && (
                      <p className="text-red-500 text-sm mt-1">{errors.grade.message}</p>
                    )}
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Feedback
                    </label>
                    <textarea
                      {...register('teacher_feedback')}
                      rows={4}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                      placeholder="Provide feedback to the student..."
                    />
                  </div>

                  <div className="flex gap-3">
                    <Button
                      type="submit"
                      icon={<Save className="w-4 h-4" />}
                      loading={gradeMutation.isPending}
                      disabled={gradeMutation.isPending}
                    >
                      Submit Grade
                    </Button>
                    <Button
                      type="button"
                      variant="ghost"
                      onClick={() => setShowGradeForm(false)}
                    >
                      Cancel
                    </Button>
                  </div>
                </form>
              </div>
            </Card>
          )}
        </div>

        <div className="space-y-6">
          <Card variant="elevated">
            <Card.Header divider>
              <h2 className="text-xl font-bold text-gray-900">Student Info</h2>
            </Card.Header>
            <Card.Body>
              <div className="flex items-center gap-3 mb-4">
                <div className="p-3 bg-gray-100 rounded-full">
                  <User className="w-6 h-6 text-gray-600" />
                </div>
                <div>
                  <p className="font-medium text-gray-900">Student</p>
                  <p className="text-sm text-gray-600">ID: {submission.student_id}</p>
                </div>
              </div>
            </Card.Body>
          </Card>

          <Card variant="elevated">
            <Card.Header divider>
              <h2 className="text-xl font-bold text-gray-900">File Info</h2>
            </Card.Header>
            <Card.Body>
              <div className="space-y-3 text-sm">
                <div>
                  <p className="text-gray-600">File Type</p>
                  <p className="text-gray-900 font-medium">{submission.file_type || 'Unknown'}</p>
                </div>
                <div>
                  <p className="text-gray-600">Submitted</p>
                  <p className="text-gray-900 font-medium">
                    {format(new Date(submission.submitted_at), 'MMM dd, yyyy')}
                  </p>
                </div>
              </div>
            </Card.Body>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default SubmissionDetailPage;

import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { useNavigate, useParams } from 'react-router-dom';
import {
  ArrowLeft,
  Calendar,
  BookOpen,
  Users,
  Edit,
  Trash2,
  Upload,
  Eye,
  CheckCircle,
  Clock,
  XCircle,
} from 'lucide-react';
import Card from '../../components/ui/Card';
import Button from '../../components/ui/Button';
import { homeworkService, submissionService, authService } from '../../services';
import { format } from 'date-fns';

const HomeworkDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const userRole = authService.getUserRole();
  const userId = authService.getUserId();

  const { data: homework, isLoading } = useQuery({
    queryKey: ['homework', id],
    queryFn: () => homeworkService.getHomework(id!),
    enabled: !!id,
  });

  const { data: submissions = [] } = useQuery({
    queryKey: ['homework-submissions', id],
    queryFn: () => homeworkService.getHomeworkSubmissions(id!),
    enabled: !!id && userRole === 'teacher',
  });

  const { data: mySubmission } = useQuery({
    queryKey: ['my-submission', id, userId],
    queryFn: async () => {
      const allSubmissions = await submissionService.getSubmissions({
        homework_id: id!,
        student_id: userId!,
      });
      return allSubmissions[0];
    },
    enabled: !!id && !!userId && userRole === 'student',
  });

  const handleDelete = async () => {
    if (window.confirm('Are you sure you want to delete this homework?')) {
      try {
        await homeworkService.deleteHomework(id!);
        navigate('/homework');
      } catch (error) {
        console.error('Failed to delete homework:', error);
        alert('Failed to delete homework');
      }
    }
  };

  const getSubmissionStatusIcon = (status: string) => {
    switch (status) {
      case 'graded':
        return <CheckCircle className="w-5 h-5 text-green-500" />;
      case 'reviewed':
        return <Eye className="w-5 h-5 text-blue-500" />;
      case 'pending':
        return <Clock className="w-5 h-5 text-yellow-500" />;
      default:
        return <XCircle className="w-5 h-5 text-gray-400" />;
    }
  };

  const getSubmissionStatusBadge = (status: string) => {
    const badges = {
      graded: 'bg-green-100 text-green-700',
      reviewed: 'bg-blue-100 text-blue-700',
      pending: 'bg-yellow-100 text-yellow-700',
    };
    return badges[status as keyof typeof badges] || 'bg-gray-100 text-gray-700';
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

  const submittedCount = submissions.filter((s: any) => s.status !== 'pending').length;
  const gradedCount = submissions.filter((s: any) => s.status === 'graded').length;

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <Button
          variant="ghost"
          icon={<ArrowLeft className="w-5 h-5" />}
          onClick={() => navigate('/homework')}
        >
          Back
        </Button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <Card variant="elevated">
            <div className="p-6">
              <div className="flex items-start justify-between mb-4">
                <div className="flex-1">
                  <h1 className="text-3xl font-bold text-gray-900 mb-2">
                    {homework.title}
                  </h1>
                  {homework.description && (
                    <p className="text-gray-600 leading-relaxed">
                      {homework.description}
                    </p>
                  )}
                </div>
                {userRole === 'teacher' && (
                  <div className="flex items-center gap-2 ml-4">
                    <Button
                      size="sm"
                      variant="secondary"
                      icon={<Edit className="w-4 h-4" />}
                      onClick={() => navigate(`/homework/${id}/edit`)}
                    >
                      Edit
                    </Button>
                    <Button
                      size="sm"
                      variant="danger"
                      icon={<Trash2 className="w-4 h-4" />}
                      onClick={handleDelete}
                    >
                      Delete
                    </Button>
                  </div>
                )}
              </div>

              <div className="flex flex-wrap gap-4 text-sm text-gray-600">
                <div className="flex items-center gap-2">
                  <Calendar className="w-4 h-4" />
                  <span>
                    Due: {format(new Date(homework.due_date), 'MMMM dd, yyyy')}
                  </span>
                </div>
                {homework.page_numbers && (
                  <div className="flex items-center gap-2">
                    <BookOpen className="w-4 h-4" />
                    <span>Pages: {homework.page_numbers}</span>
                  </div>
                )}
                {userRole === 'teacher' && (
                  <div className="flex items-center gap-2">
                    <Users className="w-4 h-4" />
                    <span>{submissions.length} student(s)</span>
                  </div>
                )}
              </div>
            </div>
          </Card>

          {userRole === 'student' && (
            <Card variant="elevated">
              <Card.Header divider>
                <h2 className="text-xl font-bold text-gray-900">Your Submission</h2>
              </Card.Header>
              <div className="p-6">
                {mySubmission ? (
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-sm text-gray-600">Status</p>
                        <div className="flex items-center gap-2 mt-1">
                          {getSubmissionStatusIcon(mySubmission.status)}
                          <span
                            className={`px-2 py-1 text-xs font-medium rounded-full ${getSubmissionStatusBadge(
                              mySubmission.status
                            )}`}
                          >
                            {mySubmission.status.charAt(0).toUpperCase() +
                              mySubmission.status.slice(1)}
                          </span>
                        </div>
                      </div>
                      {mySubmission.grade !== undefined && (
                        <div className="text-center">
                          <p className="text-sm text-gray-600">Grade</p>
                          <p className="text-3xl font-bold text-gray-900 mt-1">
                            {mySubmission.grade}
                          </p>
                        </div>
                      )}
                    </div>
                    <div>
                      <p className="text-sm text-gray-600">Submitted</p>
                      <p className="text-gray-900 mt-1">
                        {format(new Date(mySubmission.submitted_at), 'MMMM dd, yyyy hh:mm a')}
                      </p>
                    </div>
                    {mySubmission.teacher_feedback && (
                      <div>
                        <p className="text-sm text-gray-600 mb-2">Teacher Feedback</p>
                        <div className="p-4 bg-blue-50 border border-blue-100 rounded-lg">
                          <p className="text-gray-700">{mySubmission.teacher_feedback}</p>
                        </div>
                      </div>
                    )}
                    <Button
                      fullWidth
                      variant="secondary"
                      icon={<Eye className="w-4 h-4" />}
                      onClick={() => navigate(`/submissions/${mySubmission.id}`)}
                    >
                      View Submission Details
                    </Button>
                  </div>
                ) : (
                  <div className="text-center py-8">
                    <Upload className="w-12 h-12 mx-auto mb-3 text-gray-300" />
                    <p className="text-gray-500 mb-4">
                      You haven't submitted this homework yet
                    </p>
                    <Button
                      icon={<Upload className="w-4 h-4" />}
                      onClick={() => navigate(`/homework/${id}/submit`)}
                    >
                      Submit Homework
                    </Button>
                  </div>
                )}
              </div>
            </Card>
          )}

          {userRole === 'teacher' && (
            <Card variant="elevated">
              <Card.Header divider>
                <div className="flex items-center justify-between">
                  <h2 className="text-xl font-bold text-gray-900">Submissions</h2>
                  <span className="text-sm text-gray-500">
                    {submittedCount} / {submissions.length} submitted
                  </span>
                </div>
              </Card.Header>
              <div>
                {submissions.length > 0 ? (
                  submissions.map((submission: any) => (
                    <div
                      key={submission.id}
                      className="flex items-center justify-between p-4 hover:bg-gray-50 transition-colors border-b border-gray-100 last:border-0"
                    >
                      <div className="flex items-center gap-3 flex-1">
                        {getSubmissionStatusIcon(submission.status)}
                        <div>
                          <p className="font-medium text-gray-900">
                            {submission.student_name || 'Student'}
                          </p>
                          <p className="text-sm text-gray-500">
                            {submission.submitted_at
                              ? format(
                                  new Date(submission.submitted_at),
                                  'MMM dd, yyyy hh:mm a'
                                )
                              : 'Not submitted'}
                          </p>
                        </div>
                      </div>
                      <div className="flex items-center gap-3">
                        {submission.grade !== undefined && (
                          <div className="text-center">
                            <p className="text-2xl font-bold text-gray-900">
                              {submission.grade}
                            </p>
                            <p className="text-xs text-gray-500">Grade</p>
                          </div>
                        )}
                        <span
                          className={`px-2 py-1 text-xs font-medium rounded-full ${getSubmissionStatusBadge(
                            submission.status
                          )}`}
                        >
                          {submission.status.charAt(0).toUpperCase() +
                            submission.status.slice(1)}
                        </span>
                        <Button
                          size="sm"
                          variant="ghost"
                          icon={<Eye className="w-4 h-4" />}
                          onClick={() => navigate(`/submissions/${submission.id}`)}
                        >
                          View
                        </Button>
                      </div>
                    </div>
                  ))
                ) : (
                  <div className="p-8 text-center text-gray-500">
                    <Users className="w-12 h-12 mx-auto mb-3 text-gray-300" />
                    <p>No submissions yet</p>
                  </div>
                )}
              </div>
            </Card>
          )}
        </div>

        <div className="space-y-6">
          <Card variant="elevated">
            <Card.Header divider>
              <h2 className="text-xl font-bold text-gray-900">Details</h2>
            </Card.Header>
            <Card.Body>
              <div className="space-y-4">
                <div>
                  <p className="text-sm text-gray-600">Created</p>
                  <p className="text-gray-900 mt-1">
                    {format(new Date(homework.created_at), 'MMMM dd, yyyy')}
                  </p>
                </div>
                <div>
                  <p className="text-sm text-gray-600">Due Date</p>
                  <p className="text-gray-900 mt-1">
                    {format(new Date(homework.due_date), 'MMMM dd, yyyy')}
                  </p>
                </div>
                {homework.page_numbers && (
                  <div>
                    <p className="text-sm text-gray-600">Pages</p>
                    <p className="text-gray-900 mt-1">{homework.page_numbers}</p>
                  </div>
                )}
              </div>
            </Card.Body>
          </Card>

          {userRole === 'teacher' && (
            <Card variant="elevated">
              <Card.Header divider>
                <h2 className="text-xl font-bold text-gray-900">Statistics</h2>
              </Card.Header>
              <Card.Body>
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-600">Total Students</span>
                    <span className="text-lg font-bold text-gray-900">
                      {submissions.length}
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-600">Submitted</span>
                    <span className="text-lg font-bold text-gray-900">
                      {submittedCount}
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-600">Graded</span>
                    <span className="text-lg font-bold text-gray-900">
                      {gradedCount}
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-600">Pending</span>
                    <span className="text-lg font-bold text-gray-900">
                      {submissions.length - submittedCount}
                    </span>
                  </div>
                </div>
              </Card.Body>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
};

export default HomeworkDetailPage;

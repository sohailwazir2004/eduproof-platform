import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';
import {
  Search,
  Filter,
  Eye,
  CheckCircle,
  Clock,
  FileText,
  Calendar,
} from 'lucide-react';
import Card from '../../components/ui/Card';
import Button from '../../components/ui/Button';
import { submissionService, homeworkService } from '../../services';
import { SubmissionFilters } from '../../types';
import { format } from 'date-fns';

const SubmissionListPage: React.FC = () => {
  const navigate = useNavigate();

  const [searchQuery, setSearchQuery] = useState('');
  const [filters, setFilters] = useState<SubmissionFilters>({
    status: undefined,
    homework_id: undefined,
    student_id: undefined,
  });
  const [showFilters, setShowFilters] = useState(false);

  const { data: homework = [] } = useQuery({
    queryKey: ['all-homework'],
    queryFn: () => homeworkService.getHomeworkList({ limit: 100 }),
  });

  const { data: submissions = [], isLoading, refetch } = useQuery({
    queryKey: ['submissions-list', filters],
    queryFn: () => submissionService.getSubmissions(filters),
  });

  const getStatusBadge = (status: string) => {
    const badges = {
      graded: { bg: 'bg-green-100', text: 'text-green-700', icon: CheckCircle },
      reviewed: { bg: 'bg-blue-100', text: 'text-blue-700', icon: Eye },
      pending: { bg: 'bg-yellow-100', text: 'text-yellow-700', icon: Clock },
    };
    const badge = badges[status as keyof typeof badges] || badges.pending;
    const Icon = badge.icon;

    return (
      <span className={`inline-flex items-center gap-1 px-2 py-1 text-xs font-medium rounded-full ${badge.bg} ${badge.text}`}>
        <Icon className="w-3 h-3" />
        {status.charAt(0).toUpperCase() + status.slice(1)}
      </span>
    );
  };

  const getGradeColor = (grade: number) => {
    if (grade >= 90) return 'text-green-600';
    if (grade >= 80) return 'text-blue-600';
    if (grade >= 70) return 'text-yellow-600';
    return 'text-red-600';
  };

  const filteredSubmissions = submissions.filter((sub) => {
    const searchLower = searchQuery.toLowerCase();
    return (
      searchLower === '' ||
      (sub.student_id && sub.student_id.toLowerCase().includes(searchLower))
    );
  });

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Submissions</h1>
        <p className="text-gray-600 mt-1">
          {filteredSubmissions.length} submission{filteredSubmissions.length !== 1 ? 's' : ''}
        </p>
      </div>

      <Card variant="elevated" className="p-4">
        <div className="flex flex-col md:flex-row gap-4">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input
              type="text"
              placeholder="Search submissions..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
            />
          </div>
          <Button
            variant="secondary"
            icon={<Filter className="w-5 h-5" />}
            onClick={() => setShowFilters(!showFilters)}
          >
            Filters
          </Button>
        </div>

        {showFilters && (
          <div className="mt-4 pt-4 border-t border-gray-200 grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Status
              </label>
              <select
                value={filters.status || ''}
                onChange={(e) =>
                  setFilters({ ...filters, status: e.target.value || undefined })
                }
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
              >
                <option value="">All Statuses</option>
                <option value="pending">Pending</option>
                <option value="reviewed">Reviewed</option>
                <option value="graded">Graded</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Homework
              </label>
              <select
                value={filters.homework_id || ''}
                onChange={(e) =>
                  setFilters({ ...filters, homework_id: e.target.value || undefined })
                }
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
              >
                <option value="">All Homework</option>
                {homework.map((hw) => (
                  <option key={hw.id} value={hw.id}>
                    {hw.title}
                  </option>
                ))}
              </select>
            </div>

            <div className="flex items-end">
              <Button
                variant="ghost"
                fullWidth
                onClick={() =>
                  setFilters({
                    status: undefined,
                    homework_id: undefined,
                    student_id: undefined,
                  })
                }
              >
                Clear Filters
              </Button>
            </div>
          </div>
        )}
      </Card>

      {isLoading ? (
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
        </div>
      ) : filteredSubmissions.length > 0 ? (
        <div className="grid grid-cols-1 gap-4">
          {filteredSubmissions.map((submission) => (
            <Card
              key={submission.id}
              variant="elevated"
              className="p-6 hover:shadow-lg transition-shadow"
            >
              <div className="flex items-center justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <h3 className="text-lg font-semibold text-gray-900">
                      Student ID: {submission.student_id}
                    </h3>
                    {getStatusBadge(submission.status)}
                  </div>
                  <p className="text-sm text-gray-600 mb-3">
                    Homework ID: {submission.homework_id}
                  </p>
                  <div className="flex items-center gap-6 text-sm text-gray-500">
                    <div className="flex items-center gap-1">
                      <Calendar className="w-4 h-4" />
                      <span>
                        Submitted: {format(new Date(submission.submitted_at), 'MMM dd, yyyy hh:mm a')}
                      </span>
                    </div>
                    {submission.reviewed_at && (
                      <div className="flex items-center gap-1">
                        <CheckCircle className="w-4 h-4" />
                        <span>
                          Reviewed: {format(new Date(submission.reviewed_at), 'MMM dd, yyyy')}
                        </span>
                      </div>
                    )}
                  </div>
                  {submission.teacher_feedback && (
                    <div className="mt-3 p-3 bg-blue-50 border border-blue-100 rounded-lg">
                      <p className="text-sm text-gray-700">{submission.teacher_feedback}</p>
                    </div>
                  )}
                </div>
                <div className="flex items-center gap-4 ml-6">
                  {submission.grade !== undefined && (
                    <div className="text-center">
                      <p className={`text-3xl font-bold ${getGradeColor(submission.grade)}`}>
                        {submission.grade}
                      </p>
                      <p className="text-xs text-gray-500">Grade</p>
                    </div>
                  )}
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
            </Card>
          ))}
        </div>
      ) : (
        <Card variant="elevated" className="p-12 text-center">
          <FileText className="w-16 h-16 mx-auto mb-4 text-gray-300" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            No submissions found
          </h3>
          <p className="text-gray-500">
            {searchQuery || filters.homework_id || filters.status
              ? 'Try adjusting your search or filters'
              : 'Submissions will appear here once students submit their homework'}
          </p>
        </Card>
      )}
    </div>
  );
};

export default SubmissionListPage;

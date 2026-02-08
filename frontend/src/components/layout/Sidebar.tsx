import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  Home,
  BookOpen,
  FileText,
  Upload,
  BarChart3,
  Users,
  GraduationCap,
  X,
} from 'lucide-react';
import { useAuth } from '../../hooks/useAuth';

interface SidebarProps {
  isOpen: boolean;
  onClose: () => void;
}

interface MenuItem {
  path: string;
  label: string;
  icon: React.ReactNode;
  roles: string[];
}

const menuItems: MenuItem[] = [
  {
    path: '/dashboard',
    label: 'Dashboard',
    icon: <Home size={20} />,
    roles: ['student', 'teacher', 'parent', 'principal'],
  },
  {
    path: '/homework',
    label: 'Homework',
    icon: <FileText size={20} />,
    roles: ['student', 'teacher'],
  },
  {
    path: '/submissions',
    label: 'Submissions',
    icon: <Upload size={20} />,
    roles: ['student', 'teacher'],
  },
  {
    path: '/textbooks',
    label: 'Textbooks',
    icon: <BookOpen size={20} />,
    roles: ['teacher', 'principal'],
  },
  {
    path: '/classes',
    label: 'Classes',
    icon: <GraduationCap size={20} />,
    roles: ['teacher', 'principal'],
  },
  {
    path: '/students',
    label: 'Students',
    icon: <Users size={20} />,
    roles: ['teacher', 'principal'],
  },
  {
    path: '/analytics',
    label: 'Analytics',
    icon: <BarChart3 size={20} />,
    roles: ['teacher', 'parent', 'principal'],
  },
];

const Sidebar: React.FC<SidebarProps> = ({ isOpen, onClose }) => {
  const { user } = useAuth();

  const filteredMenuItems = menuItems.filter((item) =>
    item.roles.includes(user?.role || '')
  );

  return (
    <>
      {isOpen && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden"
          onClick={onClose}
        />
      )}

      <aside
        className={`
          fixed lg:sticky top-0 left-0 h-screen
          bg-white border-r border-gray-200
          w-64 transition-transform duration-300 ease-in-out
          z-50 lg:z-30
          ${isOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}
        `}
      >
        <div className="flex flex-col h-full">
          <div className="flex items-center justify-between p-4 border-b border-gray-200 lg:hidden">
            <span className="text-lg font-semibold text-gray-900">Menu</span>
            <button
              onClick={onClose}
              className="p-2 rounded-md text-gray-600 hover:bg-gray-100"
            >
              <X size={20} />
            </button>
          </div>

          <nav className="flex-1 overflow-y-auto py-4">
            <ul className="space-y-1 px-3">
              {filteredMenuItems.map((item) => (
                <li key={item.path}>
                  <NavLink
                    to={item.path}
                    onClick={onClose}
                    className={({ isActive }) =>
                      `flex items-center gap-3 px-3 py-2 rounded-lg transition-colors ${
                        isActive
                          ? 'bg-primary-50 text-primary-700 font-medium'
                          : 'text-gray-700 hover:bg-gray-100'
                      }`
                    }
                  >
                    {item.icon}
                    <span>{item.label}</span>
                  </NavLink>
                </li>
              ))}
            </ul>
          </nav>

          <div className="p-4 border-t border-gray-200">
            <div className="text-xs text-gray-500 text-center">
              EduProof v1.0.0
            </div>
          </div>
        </div>
      </aside>
    </>
  );
};

export default Sidebar;

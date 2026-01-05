import { useAuthStore } from '../store/authStore';
import { useNavigate } from 'react-router-dom';

export function Layout({ children }: { children: React.ReactNode }) {
  const { user, logout } = useAuthStore();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-bold text-gray-900">
                Zorvan Bot - Class Audio Organizer
              </h1>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-700">{user?.email}</span>
              {user?.is_admin && (
                <button
                  onClick={() => navigate('/admin')}
                  className="text-sm text-blue-600 hover:text-blue-800"
                >
                  Admin Panel
                </button>
              )}
              <button
                onClick={() => navigate('/profile')}
                className="text-sm text-blue-600 hover:text-blue-800"
              >
                Profile
              </button>
              <button
                onClick={handleLogout}
                className="px-4 py-2 text-sm font-medium text-white bg-red-600 rounded-md hover:bg-red-700"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </nav>
      <main className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
        {children}
      </main>
    </div>
  );
}

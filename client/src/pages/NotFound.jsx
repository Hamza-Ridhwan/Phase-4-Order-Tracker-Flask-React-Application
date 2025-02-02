
function NotFound() {
  return (
    <div className="text-center mt-20">
      <h2 className="text-3xl font-bold">404 - Page Not Found</h2>
      <p className="mt-2">The page you are looking for does not exist.</p>
      <Link to="/" className="text-blue-600 mt-4 inline-block">Go Back Home</Link>
    </div>
  );
}

export default NotFound;

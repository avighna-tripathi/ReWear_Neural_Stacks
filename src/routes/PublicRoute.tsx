import React from "react";
import { Navigate } from "react-router-dom";

interface PublicRouteProps {
  children: React.ReactNode;
}

const PublicRoute = ({ children }: PublicRouteProps) => {
  const isLoggedIn = !!localStorage.getItem("token");

  return isLoggedIn ? <Navigate to="/dashboard" replace /> : <>{children}</>;
};

export default PublicRoute;

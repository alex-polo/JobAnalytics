export interface Role {
  id: number;
  name: string;
  title: string;
  is_active: boolean;
}

export interface UserRoleAssignment {
  role: Role;
}

export interface UserProfile {
  first: string | null;
  last: string | null;
  avatar_url: string | null;
}

export interface User {
  id: number;
  email: string;
  is_active: boolean;
  is_verified: boolean;
  profile: UserProfile | null;
  roles_assignments: UserRoleAssignment[];
}

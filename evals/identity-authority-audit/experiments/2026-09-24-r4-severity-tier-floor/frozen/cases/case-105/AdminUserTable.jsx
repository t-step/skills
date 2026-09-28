import { useAuth } from "../hooks/useAuth";

export function AdminUserTable({ users }) {
  const { user } = useAuth();
  const isAdmin = user.role === "admin";

  return (
    <table>
      <tbody>
        {users.map((u) => (
          <tr key={u.id}>
            <td>{u.email}</td>
            <td>
              {isAdmin && (
                <button onClick={() => deleteUser(u.id)}>Delete user</button>
              )}
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

async function deleteUser(userId) {
  await fetch(`/api/users/${userId}`, {
    method: "DELETE",
    credentials: "include",
  });
}

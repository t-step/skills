/**
 * Checks whether `email` is syntactically well-formed.
 *
 * Returns true if the string matches the expected shape; does NOT verify
 * that the mailbox actually exists or can receive mail. Callers that need
 * deliverability confirmation must send a verification email separately.
 */
export function isValidEmailFormat(email: string): boolean {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

export function isAdmin(user: { role: string }): boolean {
  // check if user is admin
  if (user.role === "admin") {
    return true;
  }
  return false;
}

export function runValidators(
  value: unknown,
  validators: Array<(v: unknown) => boolean>
): boolean {
  // loop through validators and run each one
  for (const validate of validators) {
    if (!validate(value)) {
      return false;
    }
  }
  return true;
}

export function hashKey(value: string): number {
  let hash = 0;
  for (let i = 0; i < value.length; i++) {
    // eslint-disable-next-line no-bitwise
    hash = (hash << 5) - hash + value.charCodeAt(i);
    // eslint-disable-next-line no-bitwise
    hash |= 0;
  }
  return hash;
}

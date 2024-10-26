import itertools
import time
def main():
    start=time.time()
    target_password = "A234"  # Mot de passe à trouver
    character_set = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

    found = False

    for password_length in range(1, len(target_password) + 1):
        
        for password_attempt in generate_password_combinations(character_set, password_length):
            print(f"Testing combination: {password_attempt}")
            if password_attempt == target_password:
                print(f"Mot de passe trouvé : {password_attempt}")
                found = True
                break

        if found:
            break

    if not found:
        print("Mot de passe non trouvé.")
    print(time.time()-start)
def generate_password_combinations(character_set, length):
    for combination in itertools.product(character_set, repeat=length):
        yield ''.join(combination)

if __name__ == "__main__":
    main()
"""
Example Usage: Demonstrating CRUD Operations on Formula Database
"""
from db_config import MongoDBConnection, DB_NAME, FORMULAS_COLLECTION
from repository import FormulaRepository
from models import Formula


def example_usage():
    """Demonstrate various database operations"""
    
    print("=" * 60)
    print("Formula Database - Example Usage")
    print("=" * 60)
    
    # Connect to database
    mongo = MongoDBConnection()
    db = mongo.connect(DB_NAME)
    repo = FormulaRepository(db[FORMULAS_COLLECTION])
    
    # ===== CREATE =====
    print("\n" + "=" * 60)
    print("CREATE: Adding a new formula")
    print("=" * 60)
    
    new_formula = Formula(
        formula_id="ohms_law",
        name="Ohm's Law",
        description="Ohm's law: V = IR",
        equation="voltage = current * resistance",
        variables=["voltage", "current", "resistance"],
        variable_details=[
            {"name": "voltage", "description": "Electric potential difference", "unit": "V"},
            {"name": "current", "description": "Electric current", "unit": "A"},
            {"name": "resistance", "description": "Electrical resistance", "unit": "Ω"}
        ],
        category="electricity",
        tags=["physics", "electricity", "circuit"]
    )
    
    try:
        created = repo.create_formula(new_formula)
        print(f"✓ Created: {created['name']}")
    except Exception as e:
        print(f"⚠ Formula might already exist: {e}")
    
    # ===== READ =====
    print("\n" + "=" * 60)
    print("READ: Retrieving formulas")
    print("=" * 60)
    
    # Get specific formula
    print("\n1. Get specific formula by ID:")
    formula = repo.get_formula_by_id("kinetic_energy")
    if formula:
        print(f"   Found: {formula['name']}")
        print(f"   Description: {formula['description']}")
        print(f"   Variables: {', '.join(formula['variables'])}")
    
    # Get all formulas in a category
    print("\n2. Get all mechanics formulas:")
    mechanics_formulas = repo.get_all_formulas(category="mechanics")
    for f in mechanics_formulas:
        print(f"   - {f['name']}")
    
    # Search formulas
    print("\n3. Search for 'wave' formulas:")
    wave_formulas = repo.search_formulas("wave")
    for f in wave_formulas:
        print(f"   - {f['name']}")
    
    # Get formulas by tag
    print("\n4. Get all formulas tagged 'energy':")
    energy_formulas = repo.get_formulas_by_tag("energy")
    for f in energy_formulas:
        print(f"   - {f['name']}")
    
    # ===== UPDATE =====
    print("\n" + "=" * 60)
    print("UPDATE: Modifying formulas")
    print("=" * 60)
    
    # Update formula description
    print("\n1. Update formula description:")
    updated = repo.update_formula(
        "kinetic_energy",
        {"description": "Kinetic energy: KE = ½mv² (energy of motion)"}
    )
    print(f"   {'✓' if updated else '✗'} Updated kinetic_energy")
    
    # Add tags
    print("\n2. Add tags to formula:")
    updated = repo.add_tags("kinetic_energy", ["classical", "dynamics"])
    print(f"   {'✓' if updated else '✗'} Added tags to kinetic_energy")
    
    # Verify update
    formula = repo.get_formula_by_id("kinetic_energy")
    print(f"   Tags now: {formula['tags']}")
    
    # Remove a tag
    print("\n3. Remove a tag:")
    updated = repo.remove_tags("kinetic_energy", ["classical"])
    print(f"   {'✓' if updated else '✗'} Removed 'classical' tag")
    
    # ===== DELETE =====
    print("\n" + "=" * 60)
    print("DELETE: Removing formulas")
    print("=" * 60)
    
    print("\n1. Delete a specific formula (if we created Ohm's law):")
    deleted = repo.delete_formula("ohms_law")
    print(f"   {'✓' if deleted else '✗'} Deleted ohms_law")
    
    # ===== UTILITY OPERATIONS =====
    print("\n" + "=" * 60)
    print("UTILITY: Statistics and info")
    print("=" * 60)
    
    # Count formulas
    total = repo.count_formulas()
    print(f"\n1. Total formulas: {total}")
    
    # Get categories
    categories = repo.get_categories()
    print(f"\n2. Categories: {', '.join(categories)}")
    
    # Count by category
    print("\n3. Formulas per category:")
    for category in categories:
        count = repo.count_formulas(category)
        print(f"   {category}: {count}")
    
    # Get all tags
    all_tags = repo.get_all_tags()
    print(f"\n4. All tags: {', '.join(sorted(all_tags))}")
    
    # Close connection
    mongo.close()
    print("\n✅ Example complete!")


if __name__ == "__main__":
    example_usage()

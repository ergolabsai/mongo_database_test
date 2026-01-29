#!/usr/bin/env python3
"""
Formula Management CLI
Interactive command-line tool for managing formulas in MongoDB
"""
import sys
from db_config import MongoDBConnection, DB_NAME, FORMULAS_COLLECTION
from repository import FormulaRepository
from models import Formula
import json


class FormulaCLI:
    """Command-line interface for formula management"""
    
    def __init__(self):
        """Initialize CLI with database connection"""
        self.mongo = MongoDBConnection()
        self.db = self.mongo.connect(DB_NAME)
        self.repo = FormulaRepository(self.db[FORMULAS_COLLECTION])
        
    def close(self):
        """Close database connection"""
        self.mongo.close()
    
    def show_menu(self):
        """Display main menu"""
        print("\n" + "=" * 60)
        print("Formula Database Management")
        print("=" * 60)
        print("\n📋 MENU:")
        print("  1. List all formulas")
        print("  2. Search formulas")
        print("  3. View formula details")
        print("  4. Add new formula")
        print("  5. Update formula")
        print("  6. Delete formula")
        print("  7. Show statistics")
        print("  8. List by category")
        print("  9. List by tag")
        print("  0. Exit")
        print()
    
    def list_formulas(self):
        """List all formulas"""
        print("\n" + "=" * 60)
        print("All Formulas")
        print("=" * 60)
        
        formulas = self.repo.get_all_formulas()
        
        if not formulas:
            print("No formulas found.")
            return
        
        for f in formulas:
            print(f"\n📐 {f['name']} ({f['formula_id']})")
            print(f"   Category: {f['category']}")
            print(f"   Description: {f['description']}")
            print(f"   Variables: {', '.join(f['variables'])}")
    
    def search_formulas(self):
        """Search formulas by text"""
        print("\n" + "=" * 60)
        print("Search Formulas")
        print("=" * 60)
        
        search_term = input("\n🔍 Enter search term: ").strip()
        
        if not search_term:
            print("Search term cannot be empty.")
            return
        
        formulas = self.repo.search_formulas(search_term)
        
        if not formulas:
            print(f"\nNo formulas found matching '{search_term}'.")
            return
        
        print(f"\n✓ Found {len(formulas)} formula(s):")
        for f in formulas:
            print(f"\n  • {f['name']} ({f['formula_id']})")
            print(f"    {f['description']}")
    
    def view_formula(self):
        """View detailed formula information"""
        print("\n" + "=" * 60)
        print("View Formula Details")
        print("=" * 60)
        
        formula_id = input("\n📋 Enter formula ID: ").strip()
        
        formula = self.repo.get_formula_by_id(formula_id)
        
        if not formula:
            print(f"\n✗ Formula '{formula_id}' not found.")
            return
        
        print(f"\n{'=' * 60}")
        print(f"📐 {formula['name']}")
        print(f"{'=' * 60}")
        print(f"\nID: {formula['formula_id']}")
        print(f"Description: {formula['description']}")
        print(f"Equation: {formula['equation']}")
        print(f"Category: {formula['category']}")
        print(f"Tags: {', '.join(formula.get('tags', []))}")
        
        if formula.get('variable_details'):
            print("\nVariables:")
            for var in formula['variable_details']:
                unit = var.get('unit', 'N/A')
                desc = var.get('description', 'N/A')
                print(f"  • {var['name']}: {desc} [{unit}]")
        
        print(f"\nCreated: {formula['created_at']}")
        print(f"Updated: {formula['updated_at']}")
    
    def add_formula(self):
        """Add a new formula"""
        print("\n" + "=" * 60)
        print("Add New Formula")
        print("=" * 60)
        
        try:
            formula_id = input("\n📋 Formula ID (e.g., 'ohms_law'): ").strip()
            name = input("📝 Name: ").strip()
            description = input("📄 Description: ").strip()
            equation = input("🧮 Equation (Python syntax): ").strip()
            variables = input("📊 Variables (comma-separated): ").strip().split(',')
            variables = [v.strip() for v in variables]
            category = input("📁 Category: ").strip()
            tags = input("🏷️  Tags (comma-separated): ").strip().split(',')
            tags = [t.strip() for t in tags if t.strip()]
            
            formula = Formula(
                formula_id=formula_id,
                name=name,
                description=description,
                equation=equation,
                variables=variables,
                category=category,
                tags=tags
            )
            
            self.repo.create_formula(formula)
            print(f"\n✓ Successfully added formula '{formula_id}'!")
            
        except Exception as e:
            print(f"\n✗ Error adding formula: {e}")
    
    def update_formula(self):
        """Update an existing formula"""
        print("\n" + "=" * 60)
        print("Update Formula")
        print("=" * 60)
        
        formula_id = input("\n📋 Formula ID to update: ").strip()
        
        formula = self.repo.get_formula_by_id(formula_id)
        if not formula:
            print(f"\n✗ Formula '{formula_id}' not found.")
            return
        
        print(f"\nCurrent formula: {formula['name']}")
        print("\nWhat would you like to update?")
        print("1. Description")
        print("2. Equation")
        print("3. Category")
        print("4. Add tags")
        print("5. Remove tags")
        
        choice = input("\nChoice: ").strip()
        
        try:
            if choice == '1':
                new_desc = input("New description: ").strip()
                self.repo.update_formula(formula_id, {"description": new_desc})
                print("✓ Description updated!")
                
            elif choice == '2':
                new_eq = input("New equation: ").strip()
                self.repo.update_formula(formula_id, {"equation": new_eq})
                print("✓ Equation updated!")
                
            elif choice == '3':
                new_cat = input("New category: ").strip()
                self.repo.update_formula(formula_id, {"category": new_cat})
                print("✓ Category updated!")
                
            elif choice == '4':
                tags = input("Tags to add (comma-separated): ").strip().split(',')
                tags = [t.strip() for t in tags if t.strip()]
                self.repo.add_tags(formula_id, tags)
                print("✓ Tags added!")
                
            elif choice == '5':
                tags = input("Tags to remove (comma-separated): ").strip().split(',')
                tags = [t.strip() for t in tags if t.strip()]
                self.repo.remove_tags(formula_id, tags)
                print("✓ Tags removed!")
                
            else:
                print("Invalid choice.")
                
        except Exception as e:
            print(f"\n✗ Error updating formula: {e}")
    
    def delete_formula(self):
        """Delete a formula"""
        print("\n" + "=" * 60)
        print("Delete Formula")
        print("=" * 60)
        
        formula_id = input("\n📋 Formula ID to delete: ").strip()
        
        formula = self.repo.get_formula_by_id(formula_id)
        if not formula:
            print(f"\n✗ Formula '{formula_id}' not found.")
            return
        
        print(f"\n⚠️  You are about to delete: {formula['name']}")
        confirm = input("Type 'DELETE' to confirm: ").strip()
        
        if confirm == 'DELETE':
            self.repo.delete_formula(formula_id)
            print(f"\n✓ Formula '{formula_id}' deleted.")
        else:
            print("\n✗ Deletion cancelled.")
    
    def show_statistics(self):
        """Show database statistics"""
        print("\n" + "=" * 60)
        print("Database Statistics")
        print("=" * 60)
        
        total = self.repo.count_formulas()
        categories = self.repo.get_categories()
        tags = self.repo.get_all_tags()
        
        print(f"\n📊 Total formulas: {total}")
        print(f"📁 Categories: {len(categories)}")
        print(f"🏷️  Unique tags: {len(tags)}")
        
        print("\n📈 Formulas by category:")
        for cat in sorted(categories):
            count = self.repo.count_formulas(category=cat)
            print(f"  {cat}: {count}")
        
        print(f"\n🏷️  All tags: {', '.join(sorted(tags))}")
    
    def list_by_category(self):
        """List formulas by category"""
        print("\n" + "=" * 60)
        print("List by Category")
        print("=" * 60)
        
        categories = self.repo.get_categories()
        print("\nAvailable categories:")
        for i, cat in enumerate(sorted(categories), 1):
            count = self.repo.count_formulas(category=cat)
            print(f"  {i}. {cat} ({count})")
        
        category = input("\n📁 Enter category name: ").strip()
        
        formulas = self.repo.get_all_formulas(category=category)
        
        if not formulas:
            print(f"\nNo formulas found in category '{category}'.")
            return
        
        print(f"\n✓ {len(formulas)} formula(s) in '{category}':")
        for f in formulas:
            print(f"\n  • {f['name']} ({f['formula_id']})")
            print(f"    {f['description']}")
    
    def list_by_tag(self):
        """List formulas by tag"""
        print("\n" + "=" * 60)
        print("List by Tag")
        print("=" * 60)
        
        tags = self.repo.get_all_tags()
        print(f"\nAvailable tags: {', '.join(sorted(tags))}")
        
        tag = input("\n🏷️  Enter tag: ").strip()
        
        formulas = self.repo.get_formulas_by_tag(tag)
        
        if not formulas:
            print(f"\nNo formulas found with tag '{tag}'.")
            return
        
        print(f"\n✓ {len(formulas)} formula(s) with tag '{tag}':")
        for f in formulas:
            print(f"\n  • {f['name']} ({f['formula_id']})")
            print(f"    {f['description']}")
    
    def run(self):
        """Run the CLI"""
        print("\n🚀 Formula Database Management CLI")
        print("=" * 60)
        print(f"Connected to: {DB_NAME}")
        print(f"Total formulas: {self.repo.count_formulas()}")
        
        while True:
            self.show_menu()
            choice = input("Enter choice: ").strip()
            
            if choice == '1':
                self.list_formulas()
            elif choice == '2':
                self.search_formulas()
            elif choice == '3':
                self.view_formula()
            elif choice == '4':
                self.add_formula()
            elif choice == '5':
                self.update_formula()
            elif choice == '6':
                self.delete_formula()
            elif choice == '7':
                self.show_statistics()
            elif choice == '8':
                self.list_by_category()
            elif choice == '9':
                self.list_by_tag()
            elif choice == '0':
                print("\n👋 Goodbye!")
                break
            else:
                print("\n✗ Invalid choice. Please try again.")
            
            input("\nPress Enter to continue...")


def main():
    """Main entry point"""
    try:
        cli = FormulaCLI()
        cli.run()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted. Goodbye!")
    except Exception as e:
        print(f"\n✗ Error: {e}")
    finally:
        try:
            cli.close()
        except:
            pass


if __name__ == "__main__":
    main()

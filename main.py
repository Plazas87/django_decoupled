from uuid import UUID

from django_decoupled.domain.models import (
    Category,
    CategoryCollection,
    CategoryId,
    CategoryName,
    Document,
    DocumentCollection,
    DocumentId,
    DocumentText,
    Workspace,
    WorkspaceId,
    WorkspaceName,
)

if __name__ == "__main__":
    category_collection = CategoryCollection()
    document_collection = DocumentCollection()

    workspace_id = WorkspaceId(value=UUID("ef1ae7c0-47af-4028-a2d2-05652afbb400"))
    workspace_name = WorkspaceName(value="Workspace test")
    workspace = Workspace(
        id=workspace_id, name=workspace_name, categories=category_collection
    )

    category_id_one = CategoryId(UUID("18b75e72-a673-4814-bcf6-a031fa9bfbb9"))
    category_id_two = CategoryId(UUID("5c9d6234-9a01-49c2-9ba1-9a49722ad457"))
    category_name = CategoryName("Category name text")
    category_one = Category(
        id=category_id_one,
        name=category_name,
        workspace_id=workspace.id,
        documents=document_collection,
    )

    uuid_one = DocumentId(UUID("cd353ce1-5138-4125-bc4b-ae02a06d2746"))
    uuid_two = DocumentId(UUID("44f7c52e-17d2-4bec-814b-6eae1448238d"))
    text = DocumentText(value="test_text")
    document_one = Document(id=uuid_one, text=text, category_id=category_one.id)
    document_two = Document(id=uuid_two, text=text, category_id=category_one.id)


    workspace.add_category(category=category_one)
    workspace.add_document(document=document_one)
    workspace.add_document(document=document_two)

    for category in workspace.categories.values():
        for document in category.documents.values():
            print(document)

    print(workspace.categories)

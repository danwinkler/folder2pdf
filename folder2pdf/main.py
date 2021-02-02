import tempfile

from plumbum import local, cli
from PIL import Image
from pdfrw import PdfReader, PdfWriter, IndirectPdfDict


class ConvertFolderCommand(cli.Application):
    ALLOWED_SUFFIXES = [".jpeg", ".jpg", ".png"]

    def main(self, folder: cli.ExistingDirectory):
        paths = [p for p in folder.list() if p.suffix in self.ALLOWED_SUFFIXES]

        paths.sort()

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir_path = local.path(temp_dir)
            print("Converting images to pdfs")
            for path in paths:
                print(f"Converting {path}")
                im = Image.open(path)
                im = im.convert("RGB")
                im.save(temp_dir_path / path.basename + ".pdf")

            pdf_paths = [p for p in temp_dir_path.list() if p.suffix == ".pdf"]

            pdf_paths.sort()

            print("Concatenating PDFs")
            writer = PdfWriter()
            for page in pdf_paths:
                writer.addpages(PdfReader(str(page)).pages)

            writer.write(str(folder / "output.pdf"))


if __name__ == "__main__":
    ConvertFolderCommand.run()
